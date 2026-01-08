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
    
    def initialize_model(self, log_callback=None):
        """
        初始化Whisper模型
        
        Args:
            log_callback: 日志回调函数，用于显示日志消息
        """
        from faster_whisper import WhisperModel
        
        if log_callback:
            if self.model_path:
                log_callback(f"正在使用本地模型: {self.model_path}")
            else:
                log_callback(f"正在初始化模型 ({self.model_size})...")
        
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
                if log_callback:
                    log_callback(f"找到缓存的模型: {cache_dir}")
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
        if log_callback:
            log_callback("正在使用 GPU 加载模型...")
        try:
            # 优先使用GPU进行处理
            self.model = WhisperModel(
                model_input,
                device="cuda",
                compute_type="float16",
                num_workers=1,  # 使用 1 个工作线程，避免 GPU 内存问题
                device_index=0  # 使用第一个 GPU
            )

            if log_callback:
                log_callback("✓ 使用 GPU (CUDA) 进行处理")

        except Exception as e:
            # 如果GPU失败，再尝试CPU
            try:
                if log_callback:
                    log_callback(f"GPU初始化失败: {str(e)}，尝试使用CPU...")
                self.model = WhisperModel(
                    model_input,
                    device="cpu",
                    compute_type="float32",
                    num_workers=1,
                    cpu_threads=4  # 限制CPU线程数
                )

                if log_callback:
                    log_callback("✓ 使用 CPU 进行处理")
            except Exception as cpu_e:
                if log_callback:
                    log_callback(f"CPU初始化也失败: {str(cpu_e)}")
                raise Exception(f"模型初始化失败:\nGPU模式: {str(e)}\nCPU模式: {str(cpu_e)}\n请确保：\n1. 已安装 NVIDIA 驱动\n2. 已安装 CUDA Toolkit\n3. 已安装 cuDNN\n4. GPU 可用\n\n或者确保系统支持CPU处理")
        
        if self.model is None:
            raise Exception("模型初始化失败: model is None")

    def cleanup(self):
        """清理模型资源"""
        if self.model is not None:
            try:
                print("DEBUG: cleanup - 开始清理模型")
                # 不删除模型对象，只是将引用设为 None
                # 这样可以避免 Whisper 模型的析构函数卡死
                self.model = None
                print("DEBUG: cleanup - 模型已设为 None")
                print("DEBUG: cleanup - 清理完成（跳过 gc.collect）")
            except Exception as e:
                print(f"DEBUG: cleanup - 清理出错: {e}")
                pass  # 忽略清理过程中的错误
        else:
            print("DEBUG: cleanup - model 为 None，无需清理")

    def generate_subtitle(self, audio_file, log_callback=None):
        """
        为单个音频文件生成字幕
        
        Args:
            audio_file: 音频文件路径
            log_callback: 日志回调函数，用于显示日志消息
        """
        if not self.model:
            raise Exception("模型未初始化，请先调用 initialize_model()")

        # 生成输出文件名（只使用 SRT 格式）
        base_name = os.path.splitext(audio_file)[0]
        output_file = f"{base_name}.srt"

        try:
            # 使用模型生成字幕
            if log_callback:
                log_callback("正在分析音频...")

            # 调用transcribe，启用语言检测
            # 优化参数以提高处理速度
            segments, info = self.model.transcribe(
                audio_file,
                word_timestamps=False,  # 关闭词级时间戳，大幅提高速度
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

            # 确保segments被完全处理
            if log_callback:
                log_callback("DEBUG: 开始处理 segments...")
            
            # 限制 segments 的数量，防止无限迭代
            segments_list = []
            max_segments = 1000  # 最多处理 1000 个片段
            for i, segment in enumerate(segments):
                if i >= max_segments:
                    if log_callback:
                        log_callback(f"WARNING: 达到最大片段数量限制 ({max_segments})")
                    break
                segments_list.append(segment)

            # 不调用 gc.collect()，因为它可能导致阻塞

            if log_callback:
                log_callback("正在提取字幕片段...")

            # 检查语言检测信息
            detected_language = None
            if hasattr(info, 'language') and info.language:
                detected_language = info.language
                probability = getattr(info, 'language_probability', 0.0)
                if log_callback:
                    log_callback(f"检测到语言: {detected_language} (置信度: {probability:.2f})")
            else:
                if log_callback:
                    log_callback("语言检测信息不可用")
            
            if log_callback:
                log_callback(f"找到 {len(segments_list)} 个片段")
            
            # 语言代码映射
            language_map = {
                'ko': 'kor',  # 韩语
                'ja': 'jpn',  # 日语
                'zh': 'chn',  # 中文
                'en': 'eng',  # 英语
            }

            # 确定最终使用的语言代码
            # 如果指定了语言，直接使用指定的语言
            # 如果没有指定语言（None），使用 Whisper 自动检测的语言
            if self.language:
                # 用户指定了语言，直接使用
                final_language = self.language
                if log_callback:
                    log_callback(f"使用指定语言: {self.language}")
            else:
                # 自动检测模式，使用 Whisper 检测到的语言
                final_language = detected_language
                if log_callback:
                    log_callback(f"自动检测语言: {detected_language if detected_language else '未知'}")

            # 如果检测到语言，添加语言后缀
            if final_language and final_language in language_map:
                lang_suffix = language_map[final_language]
                output_file = f"{base_name}.whisper.[{lang_suffix}].srt"
            else:
                # 未检测到语言，使用 [none] 后缀
                output_file = f"{base_name}.whisper.[none].srt"

            if log_callback:
                log_callback(f"DEBUG: output_file = {output_file}")

            # 写入字幕文件
            if log_callback:
                log_callback(f"正在写入字幕文件: {os.path.basename(output_file)}")

            self._write_subtitle(output_file, segments_list, log_callback)

            if log_callback:
                log_callback(f"字幕文件写入完成: {os.path.basename(output_file)}")

            return output_file

        except Exception as e:
            if log_callback:
                log_callback(f"字幕生成失败: {str(e)}")
            raise
    
    def _write_subtitle(self, output_file, segments, log_callback=None):
        """
        写入字幕文件
        
        Args:
            output_file: 输出文件路径
            segments: 字幕片段列表
            log_callback: 日志回调函数，用于显示日志消息
        """
        try:
            if log_callback:
                log_callback(f"正在写入字幕文件: {os.path.basename(output_file)}")
            
            # 使用缓冲写入，避免卡死
            content_lines = []
            for i, segment in enumerate(segments, 1):
                
                start_time = segment.start
                end_time = segment.end
                
                def format_time(seconds):
                    ms = int(seconds * 1000)
                    s, ms = divmod(ms, 1000)
                    m, s = divmod(s, 60)
                    h, m = divmod(m, 60)
                    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
                
                content_lines.append(f"{i}\n")
                content_lines.append(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                content_lines.append(f"{segment.text.strip()}\n")
                content_lines.append("\n")
            
            # 一次性写入所有内容
            with open(output_file, "w", encoding="utf-8", buffering=8192) as f:
                f.writelines(content_lines)
            
            if log_callback:
                log_callback(f"字幕文件写入完成: {os.path.basename(output_file)}")
        except Exception as e:
            if log_callback:
                log_callback(f"写入字幕文件失败: {str(e)}")
            raise
    
    def batch_process(self, input_dir, progress_callback=None, log_callback=None, skip_existing=True):
        """
        批量处理音频文件，生成字幕
        
        Args:
            input_dir: 输入目录路径
            progress_callback: 进度回调函数（仅用于更新进度条，传入整数）
            log_callback: 日志回调函数（用于显示日志消息，传入字符串）
            skip_existing: 是否跳过已存在字幕的文件
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
                if log_callback:
                    log_callback("错误: 未找到MP3文件")
                return []
            
            if log_callback:
                log_callback(f"找到 {len(mp3_files)} 个MP3文件")
            
            # 检测已生成的字幕文件
            existing_files = []
            new_files = []

            for mp3_file in mp3_files:
                base_name = os.path.splitext(os.path.basename(mp3_file))[0]
                dir_name = os.path.dirname(mp3_file)

                # 检查是否存在任何 .whisper.[].srt 文件
                has_subtitle = False
                for file in os.listdir(dir_name):
                    if file.startswith(f"{base_name}.whisper.[") and file.endswith("].srt"):
                        has_subtitle = True
                        break

                if has_subtitle:
                    existing_files.append(mp3_file)
                else:
                    new_files.append(mp3_file)

            if log_callback:
                if new_files:
                    log_callback(f"未生成字幕: {len(new_files)} 个")
                if existing_files:
                    log_callback(f"已生成字幕: {len(existing_files)} 个")

            # 优先处理未生成的文件
            results = []
            all_files = new_files + existing_files  # 先处理新的，再处理已存在的

            total_files = len(all_files)
            for idx, mp3_file in enumerate(all_files):
                base_name = os.path.splitext(os.path.basename(mp3_file))[0]
                dir_name = os.path.dirname(mp3_file)

                # 更新进度条
                if progress_callback:
                    progress_value = int((idx + 1) / len(all_files) * 100)
                    progress_callback(progress_value)

                # 检查是否已存在字幕
                has_subtitle = False
                existing_subtitle = None
                for file in os.listdir(dir_name):
                    if file.startswith(f"{base_name}.whisper.[") and file.endswith("].srt"):
                        has_subtitle = True
                        existing_subtitle = os.path.join(dir_name, file)
                        break

                if has_subtitle and skip_existing:
                    # 跳过已存在的字幕
                    results.append((mp3_file, existing_subtitle, True))
                    if log_callback:
                        log_callback(f"⏭️ 跳过: {os.path.basename(mp3_file)} (已存在字幕)")
                    continue

                if log_callback:
                    log_callback(f"\n正在处理: {os.path.basename(mp3_file)} ({idx+1}/{total_files})")

                try:
                    output_file = self.generate_subtitle(mp3_file, log_callback)
                    results.append((mp3_file, output_file, True))

                    if log_callback:
                        log_callback(f"✅ 已生成: {os.path.basename(output_file)}")
                except Exception as e:
                    results.append((mp3_file, None, False))
                    if log_callback:
                        log_callback(f"❌ 处理失败: {str(e)}")
                    # 继续处理下一个文件
                    continue

            # 确保所有处理完成后再返回结果
            if log_callback:
                success_count = sum(1 for _, _, success in results if success)
                fail_count = len(results) - success_count

                log_callback(f"\n✅ 批处理完成: 总计 {len(results)}, 成功 {success_count}, 失败 {fail_count}")

            return results

        except Exception as e:
            if log_callback:
                log_callback(f"批处理过程中发生错误: {str(e)}")
            raise