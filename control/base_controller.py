import os
from PySide6.QtCore import Signal, QObject
from function.settings import ConfigManager, DEFAULT_KOR_STYLE, DEFAULT_CHN_STYLE


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
        
        # 初始化配置管理器
        self.config = ConfigManager()
        
        # 加载设置
        self.config.load_settings()
        
        # 将配置属性同步到控制器实例
        self.config.sync_to_controller(self)

    def load_settings(self):
        """从配置文件加载设置"""
        self.config.load_settings()
        self.config.sync_to_controller(self)

    def save_settings(self):
        """保存设置到配置文件"""
        self.config.sync_from_controller(self)
        self.config.save_settings()

    def refresh_parsed_styles(self):
        """刷新解析后的样式"""
        self.config.refresh_parsed_styles()
        self.config.sync_to_controller(self)

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
    
    def get_whisper_model_config(self):
        """
        获取 Whisper 模型配置
        
        Returns:
            dict: 包含模型大小和模型路径的字典
        """
        return self.config.get_whisper_model_config()