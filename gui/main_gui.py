import customtkinter as ctk
import tkinter as tk
from gui.components_gui import create_path_row
from gui.ass_gui import ASSConfigWindow
from gui.log_gui import LogComponent  # 导入新拆分的组件

class ToolboxGUI:
    def __init__(self, root, controller):
        self.root = root
        self.app = controller 
        self.fonts = {
            "normal": ("Microsoft YaHei", 12),
            "bold": ("Microsoft YaHei", 12, "bold"),
            "small": ("Microsoft YaHei", 11)
        }
        # 初始化弹窗管理器
        self.ass_manager = ASSConfigWindow(self.root, self.app, self.fonts)
        self.setup_ui()

    def setup_ui(self):
        # 主容器
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. 顶部行 (左侧模式开关，右侧主题切换)
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        self.mode_switch = ctk.CTkSegmentedButton(
            header, 
            values=["SRT2ASS", "SCRIPT"],
            command=self._on_mode_switched,
            height=30,  # 字体变大后，建议高度调至 35-40 之间
            font=("Microsoft YaHei", 14, "bold")  # 直接定义字体、大小和字重
        )
        self.mode_switch.pack(side="left")
        
        # 根据逻辑层状态初始化开关
        initial_val = "转换 ASS" if self.app.task_mode.get() == "ASS" else "生成剧本"
        self.mode_switch.set(initial_val)

        self.theme_btn = ctk.CTkSegmentedButton(
            header, 
            values=["Light", "Dark", "System"],
            command=self.theme_change, 
            height=28
        )
        self.theme_btn.pack(side="right")
        self.theme_btn.set(self.app.theme_mode)

        # 2. 路径输入行
        self.path_entry = create_path_row(self.main_frame, "源文件目录:", self.app.path_var, [
            ("👉", lambda: self.app.update_path_from_entry(self.app.path_var, self.path_entry)),
            ("👀", self.app.open_current_folder), 
            ("📂", self.app.browse_folder)
        ], self.fonts["normal"], self.fonts["small"], ("#000000", "#FFFFFF"))

        self.out_entry = create_path_row(self.main_frame, "输出位置:", self.app.output_path_var, [
            ("👉", lambda: self.app.update_path_from_entry(self.app.output_path_var, self.out_entry)),
            ("👀", self.app.open_output_folder), 
            ("📂", self.app.browse_output_folder)
        ], self.fonts["normal"], self.fonts["small"], "#3b8ed0")

        # 3. 功能开关行
        row3 = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row3.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkSwitch(row3, text="智能分卷", variable=self.app.enable_grouping).pack(side="left", padx=5)
        
        ctk.CTkButton(
            row3, text="📝 配置文件", command=self.app.open_config_file, 
            fg_color="#FBC02D", text_color="black", width=100
        ).pack(side="right", padx=(5, 0))
        
        ctk.CTkButton(
            row3, text="🎨 ASS样式配置", command=self.ass_manager.open, 
            fg_color="#D400FF", hover_color="#F57C00", width=120
        ).pack(side="right")

        # 4. 格式勾选与合并工具行
        tool_row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        tool_row.pack(fill="x", pady=(5, 0), padx=10)
        
        checkbox_frame = ctk.CTkFrame(tool_row, fg_color="transparent")
        checkbox_frame.pack(side="left")
        for text, var in [("TXT", self.app.do_txt), ("Word", self.app.do_word), ("PDF", self.app.do_pdf)]:
            ctk.CTkCheckBox(checkbox_frame, text=text, variable=var, width=70).pack(side="left")

        # 合并按钮（颜色与逻辑颜色对应）
        ctk.CTkButton(tool_row, text="PDF合并", command=self.app.start_pdf_merge_thread, fg_color="#ED1C24", width=85).pack(side="right", padx=2)
        ctk.CTkButton(tool_row, text="Word合并", command=self.app.start_win32_thread, fg_color="#2B5797", width=85).pack(side="right", padx=2)
        ctk.CTkButton(tool_row, text="TXT合并", command=self.app.start_txt_merge_thread, fg_color="#2DFB7C", text_color="black", width=85).pack(side="right", padx=2)
        ctk.CTkLabel(tool_row, text="|", text_color="gray50").pack(side="right", padx=10)

        # 5. 操作按钮行 (开始处理 + 清空日志)
        btn_row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=15, pady=(15, 5))

        self.app.start_btn = ctk.CTkButton(
            btn_row, 
            text="开始处理任务", 
            command=self.app.start_thread, 
            font=("微软雅黑", 14, "bold"), 
            height=35
        )
        self.app.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.clear_log_btn = ctk.CTkButton(
            btn_row,
            text="清空日志",
            command=self._clear_log,
            width=100,
            height=35,
            fg_color="#607D8B", 
            hover_color="#455A64"
        )
        self.clear_log_btn.pack(side="right")
        
        # 6. 进度条区域
        track_color = ("#CCCCCC", "#3d3d3d")
        self.progress = ctk.CTkProgressBar(
            self.main_frame, 
            height=20, 
            progress_color=track_color, # 初始与槽同色（隐藏绿点）
            fg_color=track_color,
            border_width=1,
            border_color=("#BBBBBB", "#2d2d2d")
        )
        self.progress.pack(fill="x", padx=15, pady=(10, 5))
        self.progress.set(0)

        # 进度条智能显色逻辑：有进度变绿，无进度变灰
        orig_set = self.progress.set
        def smart_set(value):
            if value > 0:
                self.progress.configure(progress_color="#28a745")
            else:
                self.progress.configure(progress_color=track_color)
            orig_set(value)
        self.progress.set = smart_set

        # 7. 日志区域 (对接拆分后的 LogComponent)
        self.log_area = LogComponent(self.main_frame)
        self.log_area.widget.pack(fill="both", padx=15, pady=10, expand=True)

    def _clear_log(self):
        """调用组件方法清空日志"""
        if hasattr(self, 'log_area'):
            self.log_area.clear()

    def _on_mode_switched(self, value):
        """同步切换逻辑层的任务模式"""
        mode = "ASS" if value == "转换 ASS" else "PDF"
        self.app.task_mode.set(mode)

    def theme_change(self, mode):
        """切换主题并通知原生日志组件更新"""
        ctk.set_appearance_mode(mode)
        self.app.save_theme_setting(mode)
        if hasattr(self, 'log_area'):
            self.log_area.update_theme(mode)