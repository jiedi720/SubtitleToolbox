"""
配置管理模块
负责处理应用程序的配置文件读写。
"""

import os
import sys
import configparser

# 全局常量与路径
# 使用 exe 所在的目录，确保打包后配置文件可以被修改和保存
def get_config_path():
    """获取配置文件路径，使用 exe 所在的目录"""
    # 获取 exe 所在的目录或脚本所在目录
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe
        base_dir = os.path.dirname(sys.executable)
    else:
        # 如果是开发环境
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_dir, "SubtitleToolbox.ini")

CONFIG_FILE = get_config_path()

# 默认 ASS 样式常量
DEFAULT_KOR_STYLE = "Style: KOR - Noto Serif KR,Noto Serif KR SemiBold,20,&H0026FCFF,&H000000FF,&H50000000,&H00000000,-1,0,0,0,100,100,0.1,0,1,0.6,0,2,10,10,34,1"
DEFAULT_JPN_STYLE = "Style: JPN - EPSON 太明朝体,EPSON 太明朝体Ｂ,14,&H00FFFFFF,&H000000FF,&H50000000,&H00000000,0,0,0,0,100,100,1,0,1,0.6,0,2,10,10,15,1"
DEFAULT_ENG_STYLE = "Style: ENG,Bosch Office Sans,16,&H0126FCFF,&H000000FF,&H14000000,&H00000000,0,0,0,0,100,100,0,0,1,1.8,0,2,10,10,15,1"
DEFAULT_CHN_STYLE = "Style: CHN - Drama,小米兰亭,17,&H28FFFFFF,&H000000FF,&H64000000,&H00000000,-1,0,0,0,100,100,0,0,1,0.5,0,2,10,10,15,1"

class SettingsHandler:
    """配置处理类，负责INI配置文件的读写操作"""
    
    @staticmethod
    def load_all_configs():
        """从SubtitleToolbox.ini读取所有配置
        
        Returns:
            dict: 包含所有配置的字典
        """
        # 创建支持中文的ConfigParser实例
        c = configparser.ConfigParser(
            default_section='DEFAULT',
            allow_no_value=False,
            strict=True,
            empty_lines_in_values=False,
            comment_prefixes=('#', ';'),
            inline_comment_prefixes=None,
            delimiters=('=', ':'),
            converters={},
            interpolation=None
        )
        data = {}
        
        if os.path.exists(CONFIG_FILE):
            try:
                # 使用utf-8编码读取配置文件
                c.read(CONFIG_FILE, encoding="utf-8")
                # 读取所有 section
                for section in c.sections():
                    data[section] = dict(c.items(section))
            except Exception as e:
                print(f"配置文件读取失败: {e}")
        
        return data

    @staticmethod
    def save_all_configs(config_data):
        """保存所有配置到SubtitleToolbox.ini
        
        Args:
            config_data: 包含所有配置的字典，格式为 {"section_name": {"key": "value"}}
        """
        # 创建支持中文的ConfigParser实例
        c = configparser.ConfigParser(
            default_section='DEFAULT',
            allow_no_value=False,
            strict=True,
            empty_lines_in_values=False,
            comment_prefixes=('#', ';'),
            inline_comment_prefixes=None,
            delimiters=('=', ':'),
            converters={},
            interpolation=None
        )
        
        # 写入所有 section
        for section_name, section_data in config_data.items():
            if not c.has_section(section_name):
                c.add_section(section_name)
            for key, value in section_data.items():
                c.set(section_name, key, str(value))

        # 使用utf-8编码写入配置文件
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            c.write(f)

    @staticmethod
    def parse_ass_style(style_line):
        """将ASS Style字符串解析为字典
        
        Args:
            style_line: ASS样式字符串
            
        Returns:
            dict: 解析后的样式字典
        """
        parts = style_line.replace("Style:", "").strip().split(',')
        while len(parts) < 23: 
            parts.append("0")
        
        return {
            "font": parts[1].strip(), 
            "size": parts[2].strip(), 
            "color": parts[3].strip(), 
            "bold": 1 if parts[7].strip()=="-1" else 0, 
            "ml": parts[19].strip(), 
            "mr": parts[20].strip(), 
            "mv": parts[21].strip(), 
            "raw": style_line.strip()
        }

class ConfigManager:
    """配置管理器，负责加载和保存所有应用程序配置"""
    
    def __init__(self):
        """初始化配置管理器"""
        self.config_file = CONFIG_FILE
        self.default_kor_raw = DEFAULT_KOR_STYLE
        self.default_jpn_raw = DEFAULT_JPN_STYLE
        self.default_eng_raw = DEFAULT_ENG_STYLE
        self.default_chn_raw = DEFAULT_CHN_STYLE

        # 初始化变量
        self._init_vars()
    
    def _init_vars(self):
        """初始化应用程序变量"""
        # 路径相关变量 - 每个任务模式独立的路径
        self.path_var = ""  # 当前源目录路径（根据task_mode动态获取）
        self.output_path_var = ""  # 当前输出目录路径（根据task_mode动态获取）

        # 各任务模式的独立路径配置
        self.script_dir = ""  # Script模式源目录
        self.script_output_dir = ""  # Script模式输出目录
        self.merge_dir = ""  # Merge模式源目录
        self.merge_output_dir = ""  # Merge模式输出目录
        self.srt2ass_dir = ""  # Srt2Ass模式源目录
        self.srt2ass_output_dir = ""  # Srt2Ass模式输出目录
        self.autosub_dir = ""  # AutoSub模式源目录
        self.autosub_output_dir = ""  # AutoSub模式输出目录

        # 预设相关变量
        self.ass_pattern = "韩上中下"  # 当前预设名称（中文格式）
        self.presets = {}

        # 任务相关变量
        self.task_mode = "Srt2Ass"  # 当前任务模式
        # Script 模式输出选项
        self.output2pdf = True  # 是否生成PDF
        self.output2word = True  # 是否生成Word
        self.output2txt = True  # 是否生成TXT
        # Merge 模式输出选项
        self.merge_pdf = True  # 是否合并PDF
        self.merge_word = True  # 是否合并Word
        self.merge_txt = True  # 是否合并TXT

        # 主题相关变量
        self.theme_mode = "System"  # 主题模式

        # 分卷相关设置
        self.volume_pattern = "智能"  # 分卷模式

        # Whisper 模型相关设置
        self.whisper_model = "默认"  # 当前 Whisper 模型
        self.whisper_model_path = "C:/Users/jiedi/AppData/Roaming/PotPlayerMini64/Model/faster-whisper-large-v3-turbo"  # Whisper 模型目录路径（默认值）
        self.whisper_language = "auto"  # Whisper 语言设置（"auto" 表示自动检测）
        self.whisper_engine = "GPU"  # Whisper 引擎设置（"GPU" 或 "CPU"）
        self.cuda_library_path = ""  # CUDA 库路径（用于 GPU 加速）

    def load_settings(self):
        """从配置文件加载设置"""
        data = SettingsHandler.load_all_configs()

        # 加载任务设置
        gen = data.get("General", {})
        self.task_mode = gen.get("task_mode", "Srt2Ass")

        # 加载各任务模式的路径设置
        # Script 模式路径
        script_config = data.get("Script", {})
        self.script_dir = script_config.get("script_dir", "")
        self.script_output_dir = script_config.get("script_output_dir", "")
        self.volume_pattern = script_config.get("volume_pattern", "智能")
        self.output2pdf = script_config.get("output2pdf", "True") == "True"
        self.output2word = script_config.get("output2word", "True") == "True"
        self.output2txt = script_config.get("output2txt", "True") == "True"

        # Merge 模式路径
        merge_config = data.get("Merge", {})
        self.merge_dir = merge_config.get("merge_dir", "")
        self.merge_output_dir = merge_config.get("merge_output_dir", "")
        self.merge_pdf = merge_config.get("merge_pdf", "True") == "True"
        self.merge_word = merge_config.get("merge_word", "True") == "True"
        self.merge_txt = merge_config.get("merge_txt", "True") == "True"

        # Srt2Ass 模式路径
        srt2ass_config = data.get("Srt2Ass", {})
        self.srt2ass_dir = srt2ass_config.get("srt2ass_dir", "")
        self.srt2ass_output_dir = srt2ass_config.get("srt2ass_output_dir", "")

        # AutoSub 模式路径
        autosub_config = data.get("AutoSub", {})
        self.autosub_dir = autosub_config.get("autosub_dir", "")
        self.autosub_output_dir = autosub_config.get("autosub_output_dir", "")
        default_whisper_path = "C:/Users/jiedi/AppData/Roaming/PotPlayerMini64/Model/faster-whisper-large-v3-turbo"
        raw_model_path = autosub_config.get("model_dir", default_whisper_path)
        self.whisper_model_path = os.path.normpath(raw_model_path) if raw_model_path else raw_model_path
        # 加载语言设置
        language_value = autosub_config.get("language", "auto")
        # 处理空字符串、字符串 'None' 或 None，都转换为 "auto"
        if language_value is None or language_value == "" or language_value == "None":
            self.whisper_language = "auto"
        else:
            self.whisper_language = language_value
        
        # 加载 Whisper 引擎设置
        self.whisper_engine = autosub_config.get("whisper_engine", "GPU")
        
        # 加载 CUDA 库路径
        self.cuda_library_path = autosub_config.get("cuda_library_path", "")

        # 加载主题设置
        appearance = data.get("Appearance", {})
        self.theme_mode = appearance.get("theme", "Light")

        # 根据当前任务模式设置当前路径
        self._update_current_paths()

        # 加载预设
        self._load_presets(data)
        
        # 加载当前选择的字体方案（在加载预设之后，确保presets字典已填充）
        ass_pattern_from_config = gen.get("ass_pattern", "韩上中下")
        
        # 将中文格式转换为英文格式
        preset_mapping = {
            "韩上中下": "kor_chn",
            "日上中下": "jpn_chn",
            "英上中下": "eng_chn"
        }
        self.ass_pattern = preset_mapping.get(ass_pattern_from_config, "kor_chn")
        
        # 确保当前预设存在
        if self.ass_pattern not in self.presets:
            self.ass_pattern = "kor_chn"
        
        # 刷新解析后的样式
        self.refresh_parsed_styles()

    def _update_current_paths(self):
        """根据当前任务模式更新当前路径"""
        # 根据task_mode映射到对应的路径变量
        path_mapping = {
            "Script": ("script_dir", "script_output_dir"),
            "Merge": ("merge_dir", "merge_output_dir"),
            "Srt2Ass": ("srt2ass_dir", "srt2ass_output_dir"),
            "AutoSub": ("autosub_dir", "autosub_output_dir")
        }

        if self.task_mode in path_mapping:
            dir_attr, output_dir_attr = path_mapping[self.task_mode]
            self.path_var = getattr(self, dir_attr, "")
            self.output_path_var = getattr(self, output_dir_attr, "")

    def _load_presets(self, data):
            """从配置数据中加载预设"""
            required_presets = ["kor_chn", "jpn_chn", "eng_chn"]
    
            # 定义每个预设对应的外语键名和默认样式
            lang_key_mapping = {
                "kor_chn": ("kor", self.default_kor_raw),
                "jpn_chn": ("jpn", self.default_jpn_raw),
                "eng_chn": ("eng", self.default_eng_raw)
            }
    
            # 先初始化所有必需的预设
            for preset_name in required_presets:
                lang_key, default_style = lang_key_mapping[preset_name]
                self.presets[preset_name] = {lang_key: default_style, "chn": self.default_chn_raw}
    
            # 从配置文件加载预设
            for section_name, section_data in data.items():
                # 检查是否是 Srt2Ass 预设 section
                if section_name.startswith("Srt2Ass"):
                    # 提取预设名称（去掉 "Srt2Ass_" 前缀）
                    preset_name = section_name[8:]  # "Srt2Ass_" 长度为 8
    
                    # 只处理已知的预设名称，忽略乱码或未知名称
                    if preset_name in required_presets:
                        # 获取对应的外语键名和默认样式
                        lang_key, default_style = lang_key_mapping[preset_name]
    
                        # 从 section_data 中提取样式行
                        lang_style = section_data.get(lang_key, "").strip()
                        chn_style = section_data.get("chn", "").strip()
    
                        # 如果样式为空，使用默认样式
                        if not lang_style:
                            lang_style = default_style
                        if not chn_style:
                            chn_style = self.default_chn_raw
    
                        self.presets[preset_name] = {
                            lang_key: lang_style,
                            "chn": chn_style
                        }
    
            # 确保当前预设存在
            if hasattr(self, 'ass_pattern') and self.ass_pattern not in self.presets:
                self.ass_pattern = "kor_chn"
    def save_settings(self):
        """保存设置到配置文件"""
        # 将英文格式转换为中文格式保存到配置文件
        preset_mapping = {
            "kor_chn": "韩上中下",
            "jpn_chn": "日上中下",
            "eng_chn": "英上中下"
        }
        ass_pattern_to_save = preset_mapping.get(self.ass_pattern, "韩上中下")
        
        # 准备各部分的配置
        config_data = {
            "Appearance": {
                "theme": self.theme_mode
            },
            "General": {
                "task_mode": self.task_mode,
                "ass_pattern": ass_pattern_to_save  # 保存当前选择的字体方案（中文格式）
            },
            "Script": {
                "script_dir": self.script_dir.strip() if hasattr(self, 'script_dir') else "",
                "script_output_dir": self.script_output_dir.strip() if hasattr(self, 'script_output_dir') else "",
                "volume_pattern": self.volume_pattern,
                "output2pdf": str(self.output2pdf),
                "output2word": str(self.output2word),
                "output2txt": str(self.output2txt)
            },
            "Merge": {
                "merge_dir": self.merge_dir.strip() if hasattr(self, 'merge_dir') else "",
                "merge_output_dir": self.merge_output_dir.strip() if hasattr(self, 'merge_output_dir') else "",
                "merge_pdf": str(self.merge_pdf),
                "merge_word": str(self.merge_word),
                "merge_txt": str(self.merge_txt)
            },
            "Srt2Ass": {
                "srt2ass_dir": self.srt2ass_dir.strip() if hasattr(self, 'srt2ass_dir') else "",
                "srt2ass_output_dir": self.srt2ass_output_dir.strip() if hasattr(self, 'srt2ass_output_dir') else ""
            },
            "AutoSub": {
                "autosub_dir": self.autosub_dir.strip() if hasattr(self, 'autosub_dir') else "",
                "autosub_output_dir": self.autosub_output_dir.strip() if hasattr(self, 'autosub_output_dir') else "",
                "model_dir": os.path.normpath(self.whisper_model_path) if hasattr(self, 'whisper_model_path') and self.whisper_model_path else "",
                "language": self.whisper_language if hasattr(self, 'whisper_language') else "auto",
                "whisper_engine": self.whisper_engine if hasattr(self, 'whisper_engine') else "GPU",
                "cuda_library_path": self.cuda_library_path.strip() if hasattr(self, 'cuda_library_path') else ""
            }
        }

        # 将预设作为独立的 section 保存（格式为 "Srt2Ass_预设名"）
        lang_key_mapping = {
            "kor_chn": "kor",
            "jpn_chn": "jpn",
            "eng_chn": "eng"
        }
        for preset_name, styles in self.presets.items():
            lang_key = lang_key_mapping[preset_name]
            config_data[f"Srt2Ass_{preset_name}"] = {
                lang_key: styles[lang_key],
                "chn": styles["chn"]
            }

        # 保存所有配置
        SettingsHandler.save_all_configs(config_data)

    def refresh_parsed_styles(self):
        """刷新解析后的样式"""
        curr_preset = self.presets[self.ass_pattern]
        
        # 根据预设名称确定外语键名
        lang_key_mapping = {
            "kor_chn": "kor",
            "jpn_chn": "jpn",
            "eng_chn": "eng"
        }
        lang_key = lang_key_mapping[self.ass_pattern]
        
        # 解析外语和中文样式
        self.kor_parsed = SettingsHandler.parse_ass_style(curr_preset[lang_key])
        self.chn_parsed = SettingsHandler.parse_ass_style(curr_preset["chn"])

    def get_whisper_model_config(self):
        """
        获取 Whisper 模型配置

        Returns:
            dict: 包含模型大小、模型路径和语言的字典
        """
        import os  # 将 import 移到函数开头以避免 UnboundLocalError
        model_size = "large-v3-turbo"  # 默认模型
        model_path = None
        language_value = getattr(self, 'whisper_language', "auto")  # 从属性获取语言设置
        # 将 "auto" 转换为 None，因为 Whisper 需要 None 表示自动检测
        language = None if language_value == "auto" else language_value

        # 如果选择了特定模型
        if self.whisper_model and self.whisper_model != "默认":
            model_name = self.whisper_model

            # 如果是本地模型
            if model_name.startswith("本地: "):
                local_model_name = model_name.replace("本地: ", "")

                # 优先使用用户通过SelectWhisperModel选择的模型路径
                if self.whisper_model_path and os.path.exists(self.whisper_model_path):
                    # 检查用户选择的路径是否包含模型名称（如果是具体模型目录）
                    if local_model_name.lower() in os.path.basename(self.whisper_model_path).lower():
                        model_path = self.whisper_model_path
                    else:
                        # 如果不是具体模型目录，则在用户选择的路径下查找模型子目录
                        model_dir = os.path.join(self.whisper_model_path, local_model_name)
                        if os.path.exists(model_dir):
                            # 查找模型文件
                            for f in os.listdir(model_dir):
                                # 检查是否为目录
                                item_path = os.path.join(model_dir, f)
                                if os.path.isdir(item_path):
                                    if f.endswith('_data') or f in ['assets', 'vocabulary']:
                                        model_path = model_dir
                                        break
                                    continue

                                # 检查文件扩展名
                                if (f.endswith(('.bin', '.safetensors', '.onnx', '.onnx_data')) or
                                    f == 'config.json' or f == 'tokenizer.json' or
                                    f == 'preprocessor_config.json' or f == 'generation_config.json' or
                                    f.startswith('model.') or f.startswith('vocabulary.') or
                                    f.startswith('tokenizer.') or f == 'model.onnx' or
                                    f == 'model.int8.onnx' or f == 'model.float16.onnx' or
                                    f == 'model.encoder.onnx' or f == 'model.decoder.onnx'):
                                    model_path = model_dir
                                    break
                        else:
                            # 如果在用户选择的路径下没找到，尝试在源目录下查找
                            model_dir = os.path.join(self.path_var.strip(), "models", local_model_name)
                            if os.path.exists(model_dir):
                                for f in os.listdir(model_dir):
                                    # 检查是否为目录
                                    item_path = os.path.join(model_dir, f)
                                    if os.path.isdir(item_path):
                                        if f.endswith('_data') or f in ['assets', 'vocabulary']:
                                            model_path = model_dir
                                            break
                                        continue

                                    # 检查文件扩展名
                                    if (f.endswith(('.bin', '.safetensors', '.onnx', '.onnx_data')) or
                                        f == 'config.json' or f == 'tokenizer.json' or
                                        f == 'preprocessor_config.json' or f == 'generation_config.json' or
                                        f.startswith('model.') or f.startswith('vocabulary.') or
                                        f.startswith('tokenizer.') or f == 'model.onnx' or
                                        f == 'model.int8.onnx' or f == 'model.float16.onnx' or
                                        f == 'model.encoder.onnx' or f == 'model.decoder.onnx'):
                                        model_path = model_dir
                                        break

            # 如果是预定义模型
            else:
                model_size = model_name
                # 尝试在用户设置的模型路径下查找对应模型
                if self.whisper_model_path and os.path.exists(self.whisper_model_path):
                    # 检查是否是 Hugging Face 缓存目录结构（包含 blobs, refs, snapshots）
                    dir_items = []
                    try:
                        dir_items = os.listdir(self.whisper_model_path)
                    except Exception:
                        pass

                    hf_cache_dirs = ['blobs', 'refs', 'snapshots']
                    is_hf_cache = all(item in dir_items for item in hf_cache_dirs)

                    actual_model_path = self.whisper_model_path
                    if is_hf_cache:
                        # 这是 Hugging Face 缓存目录，自动定位到 snapshots 目录下的实际模型目录
                        snapshots_dir = os.path.join(self.whisper_model_path, "snapshots")
                        if os.path.exists(snapshots_dir):
                            try:
                                snapshot_items = os.listdir(snapshots_dir)
                                snapshot_dirs = [item for item in snapshot_items
                                               if os.path.isdir(os.path.join(snapshots_dir, item))]
                                if snapshot_dirs:
                                    # 使用第一个 snapshot 目录
                                    actual_model_path = os.path.join(snapshots_dir, snapshot_dirs[0])
                            except Exception:
                                pass

                    # 检查用户选择的路径本身是否就是模型目录
                    path_basename = os.path.basename(actual_model_path).lower()
                    if model_name.lower() in path_basename or is_hf_cache:
                        # 用户选择了具体模型目录，检查该目录中是否有模型文件
                        model_files = []
                        for f in os.listdir(actual_model_path):
                            # 检查是否为目录
                            item_path = os.path.join(actual_model_path, f)
                            if os.path.isdir(item_path):
                                # 检查目录名称
                                if f.endswith('_data') or f in ['assets', 'vocabulary']:
                                    model_files.append(f)
                                continue

                            # 检查文件扩展名
                            if (f.endswith(('.bin', '.safetensors', '.onnx', '.onnx_data')) or
                                f == 'config.json' or   # config.json 是模型配置文件
                                f == 'tokenizer.json' or # tokenizer.json 是分词器文件
                                f == 'preprocessor_config.json' or  # 预处理器配置
                                f == 'generation_config.json' or  # 生成配置
                                f.startswith('model.') or  # model.* 文件
                                f.startswith('vocabulary.') or  # 词汇表文件
                                f.startswith('tokenizer.') or  # 分词器文件
                                f == 'model.onnx' or  # ONNX 模型文件
                                f == 'model.int8.onnx' or  # 量化模型
                                f == 'model.float16.onnx' or  # 半精度模型
                                f == 'model.encoder.onnx' or  # 编码器
                                f == 'model.decoder.onnx'):  # 解码器
                                model_files.append(f)

                        if model_files:
                            model_path = actual_model_path  # 使用实际模型路径
                        else:
                            model_path = None  # 没有模型文件，设为 None
                    else:
                        # 用户选择了模型主目录，查找对应模型的子目录
                        model_subdir = os.path.join(self.whisper_model_path, model_name)
                        if os.path.exists(model_subdir):
                            # 检查子目录中是否有模型文件
                            model_files = []
                            for f in os.listdir(model_subdir):
                                # 检查是否为目录
                                item_path = os.path.join(model_subdir, f)
                                if os.path.isdir(item_path):
                                    # 检查目录名称
                                    if f.endswith('_data') or f in ['assets', 'vocabulary']:
                                        model_files.append(f)
                                    continue

                                # 检查文件扩展名
                                if (f.endswith(('.bin', '.safetensors', '.onnx', '.onnx_data')) or
                                    f == 'config.json' or   # config.json 是模型配置文件
                                    f == 'tokenizer.json' or # tokenizer.json 是分词器文件
                                    f == 'preprocessor_config.json' or  # 预处理器配置
                                    f == 'generation_config.json' or  # 生成配置
                                    f.startswith('model.') or  # model.* 文件
                                    f.startswith('vocabulary.') or  # 词汇表文件
                                    f.startswith('tokenizer.') or  # 分词器文件
                                    f == 'model.onnx' or  # ONNX 模型文件
                                    f == 'model.int8.onnx' or  # 量化模型
                                    f == 'model.float16.onnx' or  # 半精度模型
                                    f == 'model.encoder.onnx' or  # 编码器
                                    f == 'model.decoder.onnx'):  # 解码器
                                    model_files.append(f)

                            if model_files:
                                model_path = model_subdir  # 使用子目录作为模型路径
                            else:
                                # 检查子目录是否是 Hugging Face 缓存目录结构
                                dir_items = []
                                try:
                                    dir_items = os.listdir(model_subdir)
                                except Exception:
                                    pass

                                hf_cache_dirs = ['blobs', 'refs', 'snapshots']
                                is_hf_cache = all(item in dir_items for item in hf_cache_dirs)

                                if is_hf_cache:
                                    # 这是 Hugging Face 缓存目录，自动定位到 snapshots 目录下的实际模型目录
                                    snapshots_dir = os.path.join(model_subdir, "snapshots")
                                    if os.path.exists(snapshots_dir):
                                        try:
                                            snapshot_items = os.listdir(snapshots_dir)
                                            snapshot_dirs = [item for item in snapshot_items
                                                           if os.path.isdir(os.path.join(snapshots_dir, item))]
                                            if snapshot_dirs:
                                                # 使用第一个 snapshot 目录
                                                model_path = os.path.join(snapshots_dir, snapshot_dirs[0])
                                                model_files = True  # 标记为找到了模型路径
                                        except Exception:
                                            pass

                                if not model_files:
                                    model_path = None  # 没有模型文件，设为 None
                                # 检查 snapshots 目录（Hugging Face 缓存结构）
                                snapshots_dir = os.path.join(model_subdir, "snapshots")
                                if os.path.exists(snapshots_dir):
                                    # 遍历 snapshots 下的所有子目录（通常是哈希值命名的目录）
                                    for snapshot_subdir in os.listdir(snapshots_dir):
                                        snapshot_path = os.path.join(snapshots_dir, snapshot_subdir)
                                        if os.path.isdir(snapshot_path):
                                            # 检查快照目录中是否有模型文件
                                            snapshot_files = []
                                            for f in os.listdir(snapshot_path):
                                                # 检查是否为目录
                                                item_path = os.path.join(snapshot_path, f)
                                                if os.path.isdir(item_path):
                                                    if f.endswith('_data') or f in ['assets', 'vocabulary']:
                                                        snapshot_files.append(f)
                                                    continue

                                                # 检查文件扩展名
                                                if (f.endswith(('.bin', '.safetensors', '.onnx', '.onnx_data')) or
                                                    f == 'config.json' or   # config.json 是模型配置文件
                                                    f == 'tokenizer.json' or # tokenizer.json 是分词器文件
                                                    f == 'preprocessor_config.json' or  # 预处理器配置
                                                    f == 'generation_config.json' or  # 生成配置
                                                    f.startswith('model.') or  # model.* 文件
                                                    f.startswith('vocabulary.') or  # 词汇表文件
                                                    f.startswith('tokenizer.') or  # 分词器文件
                                                    f == 'model.onnx' or  # ONNX 模型文件
                                                    f == 'model.int8.onnx' or  # 量化模型
                                                    f == 'model.float16.onnx' or  # 半精度模型
                                                    f == 'model.encoder.onnx' or  # 编码器
                                                    f == 'model.decoder.onnx'):  # 解码器
                                                    snapshot_files.append(f)

                                            if snapshot_files:
                                                model_path = snapshot_path  # 使用快照目录作为模型路径
                                                break

                                if model_path is None:  # 如果仍未找到模型文件
                                    model_path = model_subdir  # 返回子目录路径，以便后续验证
                        else:
                            model_path = None  # 子目录不存在，设为 None 以使用网络下载
                else:
                    model_path = None  # 预定义模型不需要路径
        else:
            # 使用默认模型路径（whisper_model_path）
            if self.whisper_model_path and os.path.exists(self.whisper_model_path):
                model_path = self.whisper_model_path

        return {
            "model_size": model_size,
            "model_path": model_path,
            "language": language,
            "allow_download": False  # 不允许自动下载模型，需要用户手动下载
        }

    def sync_from_controller(self, controller):
        """从控制器实例同步属性到配置管理器"""
        # 路径相关变量
        self.path_var = controller.path_var
        self.output_path_var = controller.output_path_var

        # 各任务模式的独立路径
        self.script_dir = controller.script_dir if hasattr(controller, 'script_dir') else ""
        self.script_output_dir = controller.script_output_dir if hasattr(controller, 'script_output_dir') else ""
        self.merge_dir = controller.merge_dir if hasattr(controller, 'merge_dir') else ""
        self.merge_output_dir = controller.merge_output_dir if hasattr(controller, 'merge_output_dir') else ""
        self.srt2ass_dir = controller.srt2ass_dir if hasattr(controller, 'srt2ass_dir') else ""
        self.srt2ass_output_dir = controller.srt2ass_output_dir if hasattr(controller, 'srt2ass_output_dir') else ""
        self.autosub_dir = controller.autosub_dir if hasattr(controller, 'autosub_dir') else ""
        self.autosub_output_dir = controller.autosub_output_dir if hasattr(controller, 'autosub_output_dir') else ""

        # 预设相关变量
        self.ass_pattern = controller.ass_pattern
        self.presets = controller.presets

        # 任务相关变量
        self.task_mode = controller.task_mode
        self.output2pdf = controller.output2pdf
        self.output2word = controller.output2word
        self.output2txt = controller.output2txt
        self.merge_pdf = controller.merge_pdf
        self.merge_word = controller.merge_word
        self.merge_txt = controller.merge_txt

        # 主题相关变量
        self.theme_mode = controller.theme_mode

        # 分卷相关设置
        self.volume_pattern = controller.volume_pattern
        
        # Whisper 模型相关设置
        self.whisper_model = controller.whisper_model
        self.whisper_model_path = controller.whisper_model_path
        self.whisper_language = controller.whisper_language if hasattr(controller, 'whisper_language') else "auto"

    def sync_to_controller(self, controller):
        """将配置管理器的属性同步到控制器实例"""
        # 路径相关变量
        controller.path_var = self.path_var
        controller.output_path_var = self.output_path_var

        # 各任务模式的独立路径
        controller.script_dir = self.script_dir if hasattr(self, 'script_dir') else ""
        controller.script_output_dir = self.script_output_dir if hasattr(self, 'script_output_dir') else ""
        controller.merge_dir = self.merge_dir if hasattr(self, 'merge_dir') else ""
        controller.merge_output_dir = self.merge_output_dir if hasattr(self, 'merge_output_dir') else ""
        controller.srt2ass_dir = self.srt2ass_dir if hasattr(self, 'srt2ass_dir') else ""
        controller.srt2ass_output_dir = self.srt2ass_output_dir if hasattr(self, 'srt2ass_output_dir') else ""
        controller.autosub_dir = self.autosub_dir if hasattr(self, 'autosub_dir') else ""
        controller.autosub_output_dir = self.autosub_output_dir if hasattr(self, 'autosub_output_dir') else ""

        # 预设相关变量
        controller.ass_pattern = self.ass_pattern
        controller.presets = self.presets

        # 任务相关变量
        controller.task_mode = self.task_mode
        controller.output2pdf = self.output2pdf
        controller.output2word = self.output2word
        controller.output2txt = self.output2txt
        controller.merge_pdf = self.merge_pdf
        controller.merge_word = self.merge_word
        controller.merge_txt = self.merge_txt

        # 主题相关变量
        controller.theme_mode = self.theme_mode

        # 分卷相关设置
        controller.volume_pattern = self.volume_pattern

        # Whisper 模型相关设置
        controller.whisper_model = self.whisper_model
        controller.whisper_model_path = self.whisper_model_path
        controller.whisper_language = self.whisper_language if hasattr(self, 'whisper_language') else "auto"

        # 同步解析后的样式
        controller.kor_parsed = self.kor_parsed
        controller.chn_parsed = self.chn_parsed