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
        
        # 应用保存的主题设置
        from gui.theme import apply_theme
        apply_theme(self.theme_mode)
        
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
        """更新配置：按照优先级逻辑更新GUI和配置文件"""
        # 保存当前GUI上的设定
        current_path = self.gui.ReadPathInput.text().strip()
        current_output = self.gui.SavePathInput.text().strip()
        current_ass_pattern = self.gui.AssPatternSelect.currentText()
        current_volume = self.gui.VolumePatternSelect.currentText()
        current_output2pdf = self.gui.Output2PDF.isChecked()
        current_output2word = self.gui.Output2Word.isChecked()
        current_output2txt = self.gui.Output2Txt.isChecked()
        current_merge_pdf = self.gui.MergePDF.isChecked()
        current_merge_word = self.gui.MergeWord.isChecked()
        current_merge_txt = self.gui.MergeTxt.isChecked()

        print(f"DEBUG: GUI路径 = {current_path}")
        print(f"DEBUG: GUI输出 = {current_output}")
        print(f"DEBUG: 当前模式 = {self.task_mode}")

        # 重新加载配置文件
        self.load_settings()
        self.refresh_parsed_styles()

        print(f"DEBUG: load_settings后 path_var = {self.path_var}")
        print(f"DEBUG: load_settings后 output_path_var = {self.output_path_var}")
        print(f"DEBUG: load_settings后 script_dir = {self.script_dir}")
        print(f"DEBUG: load_settings后 srt2ass_dir = {self.srt2ass_dir}")

        # 逻辑1和3：如果GUI上没有设定，则读取INI里的设定，如果都没有，那么就空着
        if not current_path:
            current_path = self.path_var
        if not current_output:
            current_output = self.output_path_var
        if not current_ass_pattern:
            # 将英文格式转换为中文格式
            preset_mapping = {
                "kor_chn": "韩上中下",
                "jpn_chn": "日上中下",
                "eng_chn": "英上中下"
            }
            current_ass_pattern = preset_mapping.get(self.ass_pattern, "韩上中下")
        if not current_volume:
            current_volume = self.volume_pattern

        print(f"DEBUG: 处理后 current_path = {current_path}")

        # 逻辑2和4：如果GUI上有设定，则保存到INI（无论INI里是否有设定）
        # 根据当前任务模式保存到对应的路径变量
        if self.task_mode == "Script":
            self.script_dir = current_path
            self.script_output_dir = current_output
            print(f"DEBUG: 设置 script_dir = {self.script_dir}")
        elif self.task_mode == "Merge":
            self.merge_dir = current_path
            self.merge_output_dir = current_output
            print(f"DEBUG: 设置 merge_dir = {self.merge_dir}")
        elif self.task_mode == "Srt2Ass":
            self.srt2ass_dir = current_path
            self.srt2ass_output_dir = current_output
            print(f"DEBUG: 设置 srt2ass_dir = {self.srt2ass_dir}")
        elif self.task_mode == "AutoSub":
            self.autosub_dir = current_path
            self.autosub_output_dir = current_output
            print(f"DEBUG: 设置 autosub_dir = {self.autosub_dir}")

        # 同时更新当前路径变量
        self.path_var = current_path
        self.output_path_var = current_output
        print(f"DEBUG: 设置 path_var = {self.path_var}")

        # 保存预设和分卷模式
        if current_ass_pattern:
            # 将中文选项转换为英文格式
            preset_mapping = {
                "韩上中下": "kor_chn",
                "日上中下": "jpn_chn",
                "英上中下": "eng_chn"
            }
            self.ass_pattern = preset_mapping.get(current_ass_pattern, "kor_chn")
        if current_volume:
            self.volume_pattern = current_volume

        # 保存更新后的配置
        print(f"DEBUG: 准备保存配置...")
        self.save_settings()
        print(f"DEBUG: 配置已保存")

        # 更新GUI界面
        if hasattr(self.gui, '_update_gui_from_settings'):
            self.gui._update_gui_from_settings()

        if hasattr(self.gui, 'log'):
            self.gui.log("配置已更新")
    
    def open_config_file(self):
        """快速打开外部配置文件 SubtitleToolbox.ini"""
        # 获取配置文件路径
        config_file = self.config.config_file
        
        # 如果配置文件不存在，先创建默认配置文件
        if not os.path.exists(config_file): 
            self.save_settings()
        
        try:
            # 使用系统默认关联程序打开配置文件
            os.startfile(config_file)
        except Exception as e:
            if hasattr(self, 'gui'):
                self.gui.log(f"❌ 无法打开配置文件: {e}")
