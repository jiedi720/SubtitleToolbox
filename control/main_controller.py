import os
from tkinter import simpledialog
import customtkinter as ctk

# 导入同级目录下的子控制器
from .base_controller import BaseController
from .ui_controller import UIController
from .task_controller import TaskController
from .tool_controller import ToolController
from gui.main_gui import ToolboxGUI

# 注意：具体的路径处理逻辑已移至 function/paths.py
# 在 TaskController 中调用任务时会触发新的分类逻辑

class UnifiedApp(BaseController, UIController, TaskController, ToolController):
    def __init__(self, root, startup_path=None, startup_out=None):
        """
        统一控制器入口：负责协调 GUI、任务执行与配置管理
        """
        # 1. 初始化基础属性 (变量、设置、主题)
        # 内部会设置 self.config_file = os.path.join(os.getcwd(), "SubtitleToolbox.ini")
        BaseController.__init__(self, root, startup_path, startup_out)
        
        # 2. 实例化 GUI 
        # root 此时已经是由入口文件设定的尺寸并居中的窗口
        self.gui = ToolboxGUI(self.root, self)
        
        # 3. 设置窗口关闭协议
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """退出前保存所有当前设置"""
        try:
            self.save_settings()
        finally:
            self.root.destroy()
        
    def save_preset_dialog(self):
        """
        保存 ASS 样式预设的弹窗逻辑
        """
        name = simpledialog.askstring(
            "保存方案", 
            "请输入新方案名称:", 
            initialvalue=self.current_preset_name.get()
        )
        
        if name and hasattr(self, 'kor_panel_ui'):
            name = name.strip()
            # 构造样式行字符串
            l_k = self.construct_style_line(self.kor_parsed["raw"], self.kor_panel_ui, "KOR")
            l_c = self.construct_style_line(self.chn_parsed["raw"], self.chn_panel_ui, "CHN")
            
            # 更新内存预设并持久化到 SubtitleToolbox.ini
            self.presets[name] = {"kor": l_k, "chn": l_c}
            self.save_settings()
            
            # 同步更新 GUI 下拉菜单
            if hasattr(self.gui.ass_manager, 'preset_combo'):
                self.gui.ass_manager.preset_combo.configure(values=list(self.presets.keys()))
                self.current_preset_name.set(name)

    def construct_style_line(self, original_raw, ui_vars, style_name):
        """
        ASS 样式行构建工具：将 UI 上的参数组装成标准的 ASS Style 字符串
        """
        # 去掉前缀并按逗号分割
        parts = original_raw.replace("Style:", "").strip().split(',')
        
        # 替换指定索引的样式参数
        parts[0] = style_name                               # 样式名
        parts[1] = ui_vars["font_var"].get()                # 字体
        parts[2] = ui_vars["size_var"].get()                # 字号
        parts[3] = ui_vars["color_var"].get()               # 主要颜色
        parts[7] = "-1" if ui_vars["bold_var"].get() else "0" # 加粗
        parts[19] = ui_vars["ml_var"].get()                 # 左边距
        parts[20] = ui_vars["mr_var"].get()                 # 右边距
        parts[21] = ui_vars["mv_var"].get()                 # 垂直边距
        
        return "Style: " + ",".join(parts)

    def save_theme_setting(self, new_theme):
        """更新主题模式（浅色/深色）并实时保存"""
        self.theme_mode = new_theme
        self.save_settings()

    def open_config_file(self):
        """
        快速打开外部配置文件 SubtitleToolbox.ini
        """
        # 如果文件丢失，先触发一次保存生成默认文件
        if not os.path.exists(self.config_file): 
            self.save_settings()
        
        try:
            # 使用系统默认关联程序打开（通常是记事本）
            os.startfile(self.config_file)
        except Exception as e:
            if hasattr(self, 'gui'):
                self.gui.log(f"❌ 无法打开配置文件: {e}")