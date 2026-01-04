import os
from PySide6.QtWidgets import QDialog, QInputDialog
from PySide6.QtCore import QObject

# 导入同级目录下的子控制器
from .base_controller import BaseController
from .ui_controller import UIController
from .task_controller import TaskController
from .tool_controller import ToolController
from gui.qt_gui import ToolboxGUI


class UnifiedApp(BaseController, UIController, TaskController, ToolController):
    """
    统一控制器类，整合了所有子控制器的功能
    负责协调GUI、任务执行与配置管理
    """
    
    def __init__(self, root, startup_path=None, startup_out=None):
        """
        初始化统一控制器
        
        Args:
            root: 根窗口对象
            startup_path: 启动时的源目录路径
            startup_out: 启动时的输出目录路径
        """
        # 初始化基础控制器，设置变量、配置和主题
        BaseController.__init__(self, root, startup_path, startup_out)
        
        # 实例化GUI
        self.gui = ToolboxGUI(self.root, self)
        
        # 设置窗口关闭事件处理
        self.gui.closeEvent = self.on_close

    def on_close(self, event):
        """窗口关闭事件处理，退出前保存所有当前设置"""
        try:
            self.save_settings()
        finally:
            event.accept()

    def save_theme_setting(self, new_theme):
        """更新主题模式并实时保存
        
        Args:
            new_theme: 新的主题模式（"Light"或"Dark"）
        """
        self.theme_mode = new_theme
        self.save_settings()

    def refresh_config_file(self):
        """刷新配置文件并更新GUI"""
        self.load_settings()
        self.refresh_parsed_styles()
        # 更新GUI界面
        if hasattr(self.gui, '_update_gui_from_settings'):
            self.gui._update_gui_from_settings()
        if hasattr(self.gui, 'log'):
            self.gui.log("配置已刷新")
    
    def save_current_directory_to_config(self):
        """将当前GUI中的目录地址保存到配置文件"""
        self.save_settings()
        if hasattr(self.gui, 'log'):
            self.gui.log("当前目录已保存到配置文件")
    
    def open_config_file(self):
        """快速打开外部配置文件 SubtitleToolbox.ini"""
        # 如果配置文件不存在，先创建默认配置文件
        if not os.path.exists(self.config_file): 
            self.save_settings()
        
        try:
            # 使用系统默认关联程序打开配置文件
            os.startfile(self.config_file)
        except Exception as e:
            if hasattr(self, 'gui'):
                self.gui.log(f"❌ 无法打开配置文件: {e}")
