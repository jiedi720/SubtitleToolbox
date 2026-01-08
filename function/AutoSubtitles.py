import os
import sys

# 在导入任何 CUDA 相关库之前就设置 DLL 路径
# 使用当前工作目录下的 venv
venv_cudnn = os.path.join(os.getcwd(), "venv", "Lib", "site-packages", "nvidia", "cudnn", "bin")
venv_cublas = os.path.join(os.getcwd(), "venv", "Lib", "site-packages", "nvidia", "cublas", "bin")

dll_paths = []
if os.path.exists(venv_cudnn):
    dll_paths.append(venv_cudnn)
    os.add_dll_directory(venv_cudnn)
if os.path.exists(venv_cublas):
    dll_paths.append(venv_cublas)
    os.add_dll_directory(venv_cublas)

if dll_paths:
    path_addition = os.pathsep.join(dll_paths)
    os.environ["PATH"] = path_addition + os.pathsep + os.environ.get("PATH", "")


class SubtitleGenerator:
    """字幕生成器核心类"""
    
    def __init__(self, model_size="large-v3-turbo", model_path=None, device="auto", language=None, allow_download=False):
        """
        初始化字幕生成器
        
        Args:
            model_size: 模型大小（如 large-v3-turbo）
            model_path: 本地模型路径（可选）
            device: 设备类型（auto/cuda/cpu）
            language: 指定语言代码（如 'ja', 'ko', 'en', 'zh'），None 表示自动检测
            allow_download: 是否允许下载模型（默认 False）
        """
        self.model_size = model_size
        self.model_path = model_path
        self.device = device
        self.language = language
        self.allow_download = allow_download
        self.model = None
        
    def initialize_model(self, progress_callback=None):
        """
        初始化Whisper模型（仅支持GPU）
        
        Args:
            progress_callback: 进度回调函数，用于报告初始化状态
        """
        from faster_whisper import WhisperModel
        
        if progress_callback:
            if self.model_path:
                progress_callback(f"正在使用本地模型: {self.model_path}")
                progress_callback("提示: 使用本地模型路径，不需要下载")
            else:
                progress_callback(f"正在初始化模型 ({self.model_size})...")
        
        # 验证模型路径
        if self.model_path and not os.path.exists(self.model_path):
            raise Exception(f"模型路径不存在: {self.model_path}")
        
        model_input = self.model_path if self.model_path else self.model_size
        
        # 如果没有指定本地模型路径，检查是否允许下载
        if not self.model_path and not self.allow_download:
            # 检查模型是否已缓存
            from huggingface_hub import snapshot_download
            try:
                cache_dir = snapshot_download(repo_id=f"Systran/{self.model_size}", local_files_only=True)
                if progress_callback:
                    progress_callback(f"找到缓存的模型: {cache_dir}")
            except Exception:
                # 模型未缓存，提示用户
                error_msg = f"未找到本地模型: {self.model_size}\n\n"
                error_msg += "请按以下步骤手动下载模型：\n"
                error_msg += "1. 访问模型下载地址: https://huggingface.co/Systran/{model_name}\n".format(model_name=self.model_size)
                error_msg += "2. 下载模型文件到本地\n"
                error_msg += "3. 在设置中指定本地模型路径\n\n"
                error_msg += "或者，在设置中允许程序自动下载模型"
                raise Exception(error_msg)
        
        # 只使用GPU处理
        if progress_callback:
            progress_callback("正在使用 GPU 加载模型...")
        
        try:
            self.model = WhisperModel(
                model_input,
                device="cuda", 
                compute_type="float16",
                num_workers=1,  # 使用 1 个工作线程，避免 GPU 内存问题
                device_index=0  # 使用第一个 GPU
            )
            
            if progress_callback:
                progress_callback("✓ 使用 GPU (CUDA) 进行处理")
                
        except Exception as e:
            if progress_callback:
                progress_callback(f"GPU初始化失败: {str(e)}")
                progress_callback("错误: 此功能仅支持 GPU，请确保已正确安装 CUDA 和 cuDNN")
            raise Exception(f"GPU初始化失败: {str(e)}\n请确保：\n1. 已安装 NVIDIA 驱动\n2. 已安装 CUDA Toolkit\n3. 已安装 cuDNN\n4. GPU 可用")
        
        if self.model is None:
            raise Exception("模型初始化失败: model is None")
    
    def generate_subtitle(self, audio_file, progress_callback=None):
        """
        为单个音频文件生成字幕
        
        Args:
            audio_file: 音频文件路径
            progress_callback: 进度回调函数
        
        Returns:
            输出文件路径
        """
        if not self.model:
            raise Exception("模型未初始化，请先调用 initialize_model()")
        
        # 生成输出文件名（只使用 SRT 格式）
        base_name = os.path.splitext(audio_file)[0]
        output_file = f"{base_name}.srt"
        
        try:
            # 使用模型生成字幕
            if progress_callback:
                progress_callback("正在分析音频...")
            
            # 调用transcribe，启用语言检测
            # 添加 beam_size 和 best_of 参数来提高速度
            segments, info = self.model.transcribe(
                audio_file,
                word_timestamps=True,
                language=self.language,  # 使用指定的语言，None 表示自动检测
                condition_on_previous_text=False,
                beam_size=1,  # 使用贪心搜索，更快
                best_of=1,    # 只采样一次，更快
                vad_filter=True,  # 启用语音活动检测
                vad_parameters=dict(min_silence_duration_ms=500),  # 最小静音 500ms
                # 提高语言检测的准确性
                language_detection_threshold=0.5,  # 语言检测阈值
                # 支持混合语言（如果音频中包含多种语言）
                # faster-whisper 会自动处理混合语言
            )
            
            if progress_callback:
                progress_callback("正在提取字幕片段...")
            
            # 转换为列表以获取实际内容
            segments_list = list(segments)
            
            # 检查语言检测信息
            detected_language = None
            if hasattr(info, 'language') and info.language:
                detected_language = info.language
                probability = getattr(info, 'language_probability', 0.0)
                if progress_callback:
                    progress_callback(f"检测到语言: {detected_language} (置信度: {probability:.2f})")
            else:
                if progress_callback:
                    progress_callback("语言检测信息不可用")
            
            if progress_callback:
                progress_callback(f"找到 {len(segments_list)} 个片段")
            
            # 语言代码映射
            language_map = {
                'ko': 'kor',  # 韩语
                'ja': 'jpn',  # 日语
                'zh': 'chn',  # 中文
                'en': 'eng',  # 英语
            }
            
            # 确定最终使用的语言代码
            final_language = self.language if self.language else detected_language
            
            # 如果没有指定语言，尝试分析字幕内容中的语言占比
            if not self.language:
                if progress_callback:
                    progress_callback("正在分析字幕语言占比...")
                
                # 简单的语言检测：根据字符特征判断
                language_counts = {
                    'ko': 0,  # 韩语：包含韩文字符
                    'ja': 0,  # 日语：包含日文字符
                    'zh': 0,  # 中文：包含中文字符
                    'en': 0,  # 英语：主要是拉丁字母
                }
                
                import re
                
                for segment in segments_list:
                    text = segment.text
                    
                    # 统计各语言字符数量
                    # 韩语范围：\uAC00-\uD7AF
                    korean_chars = len(re.findall(r'[\uAC00-\uD7AF]', text))
                    # 日语平假名：\u3040-\u309F，片假名：\u30A0-\u30FF
                    japanese_chars = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF]', text))
                    # 中文范围：\u4E00-\u9FFF
                    chinese_chars = len(re.findall(r'[\u4E00-\u9FFF]', text))
                    # 英文和其他拉丁字母
                    latin_chars = len(re.findall(r'[a-zA-Z]', text))
                    
                    language_counts['ko'] += korean_chars
                    language_counts['ja'] += japanese_chars
                    language_counts['zh'] += chinese_chars
                    language_counts['en'] += latin_chars
                
                # 找出占比最多的语言
                total_chars = sum(language_counts.values())
                if total_chars > 0:
                    max_lang = max(language_counts, key=language_counts.get)
                    max_count = language_counts[max_lang]
                    max_ratio = max_count / total_chars
                    
                    if progress_callback:
                        progress_callback(f"语言占比统计:")
                        for lang_code, count in language_counts.items():
                            if count > 0:
                                ratio = count / total_chars
                                lang_name = language_map.get(lang_code, lang_code)
                                progress_callback(f"  - {lang_name}: {ratio:.1%} ({count} 字符)")
                        progress_callback(f"主要语言: {language_map.get(max_lang, max_lang)} ({max_ratio:.1%})")
                    
                    # 如果占比最多的语言超过 30%，使用该语言
                    if max_ratio > 0.3:
                        final_language = max_lang
            else:
                if progress_callback:
                    progress_callback(f"使用指定语言: {self.language}")
            
            # 如果检测到语言，添加语言后缀
            if final_language and final_language in language_map:
                lang_suffix = language_map[final_language]
                output_file = f"{base_name}.whisper.[{lang_suffix}].srt"
                if progress_callback:
                    progress_callback(f"输出文件名: {os.path.basename(output_file)}")
            else:
                # 未检测到语言，使用 [none] 后缀
                output_file = f"{base_name}.whisper.[none].srt"
                if progress_callback:
                    progress_callback(f"未检测到语言，使用默认后缀")
                    progress_callback(f"输出文件名: {os.path.basename(output_file)}")
            
            # 写入字幕文件
            if progress_callback:
                progress_callback("正在写入字幕文件...")
            
            self._write_subtitle(output_file, segments_list, progress_callback)
            
            if progress_callback:
                progress_callback(f"字幕文件写入完成: {os.path.basename(output_file)}")
            
            return output_file
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"字幕生成失败: {str(e)}")
            raise
    
    def _write_subtitle(self, output_file, segments, progress_callback=None):
        """
        写入 SRT 格式字幕文件
        
        Args:
            output_file: 输出文件路径
            segments: 字幕片段列表
            progress_callback: 进度回调函数
        """
        with open(output_file, "w", encoding="utf-8") as f:
            # 写入SRT格式
            for i, segment in enumerate(segments, 1):
                if progress_callback:
                    progress_callback(f"处理片段 {i}/{len(segments)}")
                
                start_time = segment.start
                end_time = segment.end
                
                def format_time(seconds):
                    ms = int(seconds * 1000)
                    s, ms = divmod(ms, 1000)
                    m, s = divmod(s, 60)
                    h, m = divmod(m, 60)
                    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
                
                f.write(f"{i}\n")
                f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                f.write(f"{segment.text.strip()}\n")
                f.write("\n")
    
    def batch_process(self, input_dir, progress_callback=None):
        """
        批量处理目录中的所有MP3文件，生成SRT字幕
        
        Args:
            input_dir: 输入目录
            progress_callback: 进度回调函数
        
        Returns:
            处理的文件列表
        """
        if not self.model:
            raise Exception("模型未初始化，请先调用 initialize_model()")
        
        try:
            # 获取所有.mp3文件
            mp3_files = []
            for root, _, files in os.walk(input_dir):
                for file in files:
                    if file.lower().endswith(".mp3"):
                        mp3_files.append(os.path.join(root, file))
            
            if not mp3_files:
                if progress_callback:
                    progress_callback("错误: 未找到MP3文件")
                return []
            
            if progress_callback:
                progress_callback(f"找到 {len(mp3_files)} 个MP3文件")
            
            # 处理每个文件
            results = []
            for idx, mp3_file in enumerate(mp3_files):
                if progress_callback:
                    progress_callback(f"\n正在处理: {os.path.basename(mp3_file)} ({idx+1}/{len(mp3_files)})")
                
                try:
                    output_file = self.generate_subtitle(mp3_file, progress_callback)
                    results.append((mp3_file, output_file, True))
                    
                    if progress_callback:
                        progress_callback(f"✓ 已生成: {output_file}")
                except Exception as e:
                    results.append((mp3_file, None, False))
                    if progress_callback:
                        progress_callback(f"✗ 处理失败: {str(e)}")
                    # 继续处理下一个文件
                    continue
            
            return results
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"批处理过程中发生错误: {str(e)}")
            raise
        finally:
            # 确保清理 GPU 内存
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    if progress_callback:
                        progress_callback("已清理 GPU 缓存")
            except:
                pass