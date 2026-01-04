import os
from PySide6.QtCore import Signal, QObject
from config.settings import CONFIG_FILE, SettingsHandler, DEFAULT_KOR_STYLE, DEFAULT_CHN_STYLE
from function.volumes import init_volume_settings, load_volume_settings, save_volume_settings


class BaseController(QObject):
    """
    基础控制器类，提供应用程序的核心功能和状态管理
    继承自QObject以支持信号和槽机制
    """
    # 信号定义：用于线程安全地更新GUI
    update_log = Signal(str)  # 更新日志信号
    update_progress = Signal(int)  # 更新进度条信号
    enable_start_button = Signal(bool)  # 启用/禁用开始按钮信号
    
    def __init__(self, root, startup_path=None, startup_out=None):
        """
        初始化基础控制器
        
        Args:
            root: 根窗口对象
            startup_path: 启动时的源目录路径
            startup_out: 启动时的输出目录路径
        """
        super().__init__()
        self.root = root
        self.config_file = CONFIG_FILE
        
        # 初始化默认样式
        self.default_kor_raw = DEFAULT_KOR_STYLE
        self.default_chn_raw = DEFAULT_CHN_STYLE

        # 初始化变量和设置
        self._init_vars()
        self.load_settings()

        # 加载和处理预设
        raw_config = SettingsHandler.load_all_configs()
        self.presets = raw_config.get("Presets", {})
        if not self.presets:
            # 如果没有预设，创建默认预设
            self.presets = {"默认": {"kor": self.default_kor_raw, "chn": self.default_chn_raw}}
        
        # 确保当前预设存在
        current_name = self.current_preset_name
        if current_name not in self.presets:
            current_name = list(self.presets.keys())[0]
            self.current_preset_name = current_name
        
        # 刷新解析后的样式
        self.refresh_parsed_styles()

    def _init_vars(self):
        """初始化应用程序变量"""
        # 路径相关变量
        self.path_var = ""  # 源目录路径
        self.output_path_var = ""  # 输出目录路径
        
        # 预设相关变量
        self.current_preset_name = "默认"  # 当前预设名称
        
        # 任务相关变量
        self.task_mode = "Srt2Ass"  # 当前任务模式
        self.do_pdf = True  # 是否生成PDF
        self.do_word = True  # 是否生成Word
        self.do_txt = True  # 是否生成TXT
        
        # 主题相关变量
        self.theme_mode = "System"  # 主题模式
        
        # 分卷相关设置
        volume_settings = init_volume_settings()
        self.volume_pattern = volume_settings["volume_pattern"]  # 分卷模式

    def refresh_parsed_styles(self):
        """刷新解析后的样式"""
        curr_preset = self.presets[self.current_preset_name]
        self.kor_parsed = SettingsHandler.parse_ass_style(curr_preset["kor"])
        self.chn_parsed = SettingsHandler.parse_ass_style(curr_preset["chn"])

    def load_settings(self):
        """从配置文件加载设置"""
        data = SettingsHandler.load_all_configs()
        gen = data.get("General", {})
        
        # 加载路径设置
        self.path_var = gen.get("last_dir", "C:/")
        self.output_path_var = gen.get("custom_output_dir", "")
        
        # 加载任务设置
        self.task_mode = gen.get("task_mode", "Srt2Ass")
        self.do_pdf = gen.get("do_pdf", "True") == "True"
        self.do_word = gen.get("do_word", "True") == "True"
        self.do_txt = gen.get("do_txt", "True") == "True"
        
        # 加载分卷设置
        volume_settings = load_volume_settings(gen)
        self.volume_pattern = volume_settings["volume_pattern"]
        
        # 加载主题设置
        self.theme_mode = data.get("Appearance", {}).get("theme", "Light")

    def save_settings(self):
        """保存设置到配置文件"""
        # 准备分卷相关设置
        volume_settings = {
            "volume_pattern": self.volume_pattern
        }
        volume_config = save_volume_settings(volume_settings)
        
        # 准备通用设置
        current_gen = {
            "last_dir": self.path_var.strip(),
            "custom_output_dir": self.output_path_var.strip(),
            "task_mode": self.task_mode,
            "do_pdf": str(self.do_pdf),
            "do_word": str(self.do_word),
            "do_txt": str(self.do_txt),
            "theme": self.theme_mode
        }
        
        # 合并分卷设置到通用设置
        current_gen.update(volume_config)
        
        # 保存所有配置
        SettingsHandler.save_all_configs(current_gen, self.presets)

    def log(self, message, tag=None):
        """
        记录日志信息
        
        Args:
            message: 日志消息
            tag: 日志标签（可选）
        """
        # 使用信号线程安全地更新日志
        self.update_log.emit(message)
    
    def delete_generated_files(self):
        """删除生成的文件"""
        from function.trash import clear_output_to_trash
        
        # 获取目标目录
        target_dir = self.output_path_var.strip() or self.path_var.strip()
        if not target_dir:
            self.log("❌ 请先选择源目录或输出目录")
            return
        
        # 使用现有的清理功能
        clear_output_to_trash(target_dir, self.log)