import os


class SubtitleGenerator:
    """字幕生成器核心类"""
    
    def __init__(self, model_size="large-v3-turbo", model_path=None, device="auto"):
        """
        初始化字幕生成器
        
        Args:
            model_size: 模型大小（如 large-v3-turbo）
            model_path: 本地模型路径（可选）
            device: 设备类型（auto/cuda/cpu）
        """
        self.model_size = model_size
        self.model_path = model_path
        self.device = device
        self.model = None
        
    def initialize_model(self, progress_callback=None):
        """
        初始化Whisper模型
        
        Args:
            progress_callback: 进度回调函数，用于报告初始化状态
        """
        # 自动定位 venv 里的 nvidia 库路径并加入系统搜索
        venv_path = os.path.join(os.getcwd(), "venv", "Lib", "site-packages", "nvidia")
        if os.path.exists(venv_path):
            for root, dirs, files in os.walk(venv_path):
                if "bin" in dirs:
                    bin_dir = os.path.join(root, "bin")
                    # 核心逻辑：将 DLL 目录加入 Windows 的搜索路径
                    os.add_dll_directory(bin_dir)
                    os.environ["PATH"] = bin_dir + os.pathsep + os.environ["PATH"]
        
        from faster_whisper import WhisperModel
        
        if progress_callback:
            if self.model_path:
                progress_callback(f"正在使用本地模型: {self.model_path}")
                progress_callback("提示: 使用本地模型路径，不需要下载")
            else:
                progress_callback(f"正在初始化模型 ({self.model_size})...")
                progress_callback("提示: 首次使用需要下载模型，这可能需要几分钟时间")
        
        # 验证模型路径
        if self.model_path and not os.path.exists(self.model_path):
            raise Exception(f"模型路径不存在: {self.model_path}")
        
        model_input = self.model_path if self.model_path else self.model_size
        
        # 尝试使用GPU
        try:
            if progress_callback:
                progress_callback("尝试使用 GPU 加载模型...")
            
            self.model = WhisperModel(
                model_input,
                device="cuda", 
                compute_type="float16"
            )
            
            if progress_callback:
                progress_callback("✓ 使用 GPU (CUDA) 进行处理")
                
        except Exception as cuda_error:
            # GPU初始化失败，回退到CPU
            if progress_callback:
                progress_callback("GPU不可用，正在使用 CPU...")
            
            try:
                self.model = WhisperModel(
                    model_input,
                    device="cpu", 
                    compute_type="int8"
                )
                
                if progress_callback:
                    progress_callback("✓ 使用 CPU 进行处理（速度较慢）")
            except Exception as cpu_error:
                if progress_callback:
                    progress_callback(f"CPU初始化也失败: {str(cpu_error)}")
                raise Exception(f"模型初始化失败: GPU错误 - {str(cuda_error)}, CPU错误 - {str(cpu_error)}")
        
        if self.model is None:
            raise Exception("模型初始化失败: model is None")
    
    def generate_subtitle(self, audio_file, output_format="srt", progress_callback=None):
        """
        为单个音频文件生成字幕
        
        Args:
            audio_file: 音频文件路径
            output_format: 输出格式（srt/vtt）
            progress_callback: 进度回调函数
        
        Returns:
            输出文件路径
        """
        if not self.model:
            raise Exception("模型未初始化，请先调用 initialize_model()")
        
        # 生成输出文件名
        base_name = os.path.splitext(audio_file)[0]
        output_file = f"{base_name}.{output_format}"
        
        try:
            # 使用模型生成字幕
            if progress_callback:
                progress_callback("正在分析音频...")
            
            # 调用transcribe，启用语言检测
            segments, info = self.model.transcribe(
                audio_file, 
                word_timestamps=True,
                language=None,  # None表示自动检测语言
                condition_on_previous_text=False
            )
            
            # 转换为列表以获取实际内容
            segments_list = list(segments)
            
            # 检查语言检测信息
            if progress_callback:
                if hasattr(info, 'language') and info.language:
                    language = info.language
                    probability = getattr(info, 'language_probability', 0.0)
                    progress_callback(f"检测到语言: {language} (置信度: {probability:.2f})")
                else:
                    progress_callback("语言检测信息不可用")
                
                progress_callback(f"找到 {len(segments_list)} 个片段")
            
            # 写入字幕文件
            self._write_subtitle(output_file, segments_list, output_format, progress_callback)
            
            return output_file
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"字幕生成失败: {str(e)}")
            raise
    
    def _write_subtitle(self, output_file, segments, output_format, progress_callback=None):
        """
        写入字幕文件
        
        Args:
            output_file: 输出文件路径
            segments: 字幕片段列表
            output_format: 输出格式（srt/vtt）
            progress_callback: 进度回调函数
        """
        with open(output_file, "w", encoding="utf-8") as f:
            if output_format == "srt":
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
            
            elif output_format == "vtt":
                # 写入VTT格式
                f.write("WEBVTT\n\n")
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
                        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
                    
                    f.write(f"{i}\n")
                    f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                    f.write(f"{segment.text.strip()}\n")
                    f.write("\n")
    
    def batch_process(self, input_dir, output_format="srt", progress_callback=None):
        """
        批量处理目录中的所有MP3文件
        
        Args:
            input_dir: 输入目录
            output_format: 输出格式（srt/vtt）
            progress_callback: 进度回调函数
        
        Returns:
            处理的文件列表
        """
        if not self.model:
            raise Exception("模型未初始化，请先调用 initialize_model()")
        
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
                output_file = self.generate_subtitle(mp3_file, output_format, progress_callback)
                results.append((mp3_file, output_file, True))
                
                if progress_callback:
                    progress_callback(f"✓ 已生成: {output_file}")
            except Exception as e:
                results.append((mp3_file, None, False))
                if progress_callback:
                    progress_callback(f"✗ 处理失败: {str(e)}")
        
        return results