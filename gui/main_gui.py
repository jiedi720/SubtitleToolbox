import customtkinter as ctk
import tkinter as tk
from gui.components_gui import create_path_row
from gui.ass_gui import ASSConfigWindow
from gui.log_gui import LogComponent

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

        # 1. 顶部行 (左侧模式开关，中间配置按钮，右侧主题切换)
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        # [左侧] 模式切换
        self.mode_switch = ctk.CTkSegmentedButton(
            header, 
            values=["SRT2ASS", "SCRIPT"],
            command=self._on_mode_switched,
            height=30,
            font=("Microsoft YaHei", 14, "bold")
        )
        self.mode_switch.pack(side="left")
        
        # 初始化开关状态
        initial_val = "SRT2ASS" if self.app.task_mode.get() == "SRT2ASS" else "SCRIPT"
        self.mode_switch.set(initial_val)

        # [右侧] 主题切换 (side="right" 先pack的在最右)
        self.theme_btn = ctk.CTkSegmentedButton(
            header, 
            values=["Light", "Dark", "System"],
            command=self.theme_change, 
            height=28
        )
        self.theme_btn.pack(side="right")
        self.theme_btn.set(self.app.theme_mode)

        # [中间靠右] 配置文件按钮
        ctk.CTkButton(
            header, text="📝 配置", command=self.app.open_config_file, 
            fg_color="#FBC02D", hover_color="#C08B06", text_color="black", width=85, height=28, font=("微软雅黑", 13, "bold")
        ).pack(side="right", padx=5)
        
        # [中间靠右] ASS样式配置按钮
        ctk.CTkButton(
            header, text="🎨 ASS样式", command=self.ass_manager.open, 
            fg_color="#D851D8", hover_color="#A72DA7",text_color="black", width=85, height=28,font=("微软雅黑", 13, "bold")
        ).pack(side="right", padx=5)

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

        # 3. 格式勾选、智能分卷与合并工具行 (整合行)
        tool_row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        tool_row.pack(fill="x", pady=(10, 5), padx=10)
        
        # 左侧容器：包含复选框和智能分卷
        checkbox_frame = ctk.CTkFrame(tool_row, fg_color="transparent")
        checkbox_frame.pack(side="left", padx=(10, 0))
        
        # TXT/Word/PDF 选框
        for text, var in [("TXT", self.app.do_txt), ("Word", self.app.do_word), ("PDF", self.app.do_pdf)]:
            ctk.CTkCheckBox(
                checkbox_frame, text=text, variable=var, width=70,
                font=("微软雅黑", 13, "bold")
            ).pack(side="left")

        # 智能分卷
        ctk.CTkSwitch(
            checkbox_frame, 
            text="智能分卷", 
            variable=self.app.enable_grouping,
            font=("微软雅黑", 13, "bold")
        ).pack(side="left", padx=(25, 15))

        # [新增] 一键清空脚本目录按钮：紧跟在智能分卷右侧
        self.trash_btn = ctk.CTkButton(
            checkbox_frame, 
            text="清空剧本", 
            command=self.app.clean_script_trash,  # 确保 controller 实现了此方法
            fg_color="#767676", 
            hover_color="#989898",
            width=71,
            height=29,
            font=("微软雅黑", 13, "bold")
        )
        self.trash_btn.pack(side="left", padx=5)

        # 右侧：合并功能按钮
        ctk.CTkButton(tool_row, text="PDF合并", command=self.app.start_pdf_merge_thread, fg_color="#ED1C24", hover_color="#AF0E13", width=83).pack(side="right", padx=2)
        ctk.CTkButton(tool_row, text="Word合并", command=self.app.start_win32_thread, fg_color="#2B5797", hover_color="#1C4077", width=83).pack(side="right", padx=2)
        ctk.CTkButton(tool_row, text="TXT合并", command=self.app.start_txt_merge_thread, fg_color="#B4D0BF", text_color="black", hover_color="#799B86", width=83).pack(side="right", padx=2)

        # 4. 操作按钮行 (开始处理 + 清空日志)
        btn_row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=15, pady=(15, 5))

        self.app.start_btn = ctk.CTkButton(
            btn_row, 
            text="开始处理任务", 
            command=self.app.start_thread, 
            font=("微软雅黑", 14, "bold"), 
            height=35,
            fg_color="#038546", 
            hover_color="#024D20"
        )
        self.app.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.clear_log_btn = ctk.CTkButton(
            btn_row,
            text="清空日志",
            command=self._clear_log,
            font=("微软雅黑", 14, "bold"),
            width=100,
            height=35,
            fg_color="#607D8B", 
            hover_color="#384C55"
        )
        self.clear_log_btn.pack(side="right")
        
        # 5. 进度条区域
        track_color = ("#CCCCCC", "#3d3d3d")
        self.progress = ctk.CTkProgressBar(
            self.main_frame, 
            height=20, 
            progress_color=track_color,
            fg_color=track_color,
            border_width=1,
            border_color=("#BBBBBB", "#2d2d2d")
        )
        self.progress.pack(fill="x", padx=15, pady=(10, 5))
        self.progress.set(0)

        # 进度条显色逻辑
        orig_set = self.progress.set
        def smart_set(value):
            if value > 0:
                self.progress.configure(progress_color="#28a745")
            else:
                self.progress.configure(progress_color=track_color)
            orig_set(value)
        self.progress.set = smart_set

        # 6. 日志区域
        self.log_area = LogComponent(self.main_frame)
        self.log_area.widget.pack(fill="both", padx=15, pady=10, expand=True)

    def _clear_log(self):
        if hasattr(self, 'log_area'):
            self.log_area.clear()

    def _on_mode_switched(self, value):
        self.app.task_mode.set(value)
        if hasattr(self, 'log_area'):
            self.log_area.write_log(f"[系统] 模式已切换为: {value}")
        if hasattr(self.app, 'save_settings'):
            self.app.save_settings()

    def theme_change(self, mode):
        ctk.set_appearance_mode(mode)
        self.app.save_theme_setting(mode)
        if hasattr(self, 'log_area'):
            self.log_area.update_theme(mode)