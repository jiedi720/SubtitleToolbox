import tkinter as tk
import customtkinter as ctk
import re
from tkinter import colorchooser
from font.font import FontSelector

class ASSConfigWindow:
    def __init__(self, parent_root, app_controller, fonts):
        self.root = parent_root
        self.app = app_controller
        self.fonts = fonts
        self.window = None

    def open(self):
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = ctk.CTkToplevel(self.root)
        self.window.title("ASS样式配置")
        self.window.geometry("960x330")
        # --- 新增：窗口居中逻辑 ---
        win_w, win_h = 960, 330
        # 获取主窗口的位置和尺寸
        self.root.update_idletasks() # 确保获取到的是最新位置
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()
        
        # 计算子窗口相对于主窗口居中的坐标
        cx = int(root_x + (root_w / 2) - (win_w / 2))
        cy = int(root_y + (root_h / 2) - (win_h / 2))
        
        self.window.geometry(f"{win_w}x{win_h}+{cx}+{cy}")
        # -----------------------
        self.window.attributes("-topmost", True)

        # 1. 顶部方案管理
        top_bar = ctk.CTkFrame(self.window, fg_color="transparent")
        top_bar.pack(fill="x", padx=25, pady=15)
        ctk.CTkLabel(top_bar, text="配置方案:", font=self.fonts["bold"]).pack(side="left")
        
        self.preset_combo = ctk.CTkOptionMenu(
            top_bar, variable=self.app.current_preset_name, 
            values=list(self.app.presets.keys()), 
            command=lambda v: self.app.on_preset_change(None)
        )
        self.preset_combo.pack(side="left", padx=15)
        
        ctk.CTkButton(top_bar, text="💾 保存方案", command=self.app.save_preset_dialog, fg_color="#00BCD4", text_color="black", width=100).pack(side="left", padx=5)
        ctk.CTkButton(top_bar, text="📝 配置文件", command=self.app.open_config_file, fg_color="#FBC02D", text_color="black", width=100).pack(side="left", padx=5)

        # 2. 面板容器
        panels = ctk.CTkFrame(self.window, fg_color="transparent")
        panels.pack(fill="both", expand=True, padx=20)
        
        self.app.kor_panel_ui = self._build_panel(panels, "外语样式", self.app.kor_parsed, "안녕하세요 こんにちは Hello")
        self.app.chn_panel_ui = self._build_panel(panels, "中文样式", self.app.chn_parsed, "你好世界")

    def _build_panel(self, parent, title, data, preview_text):
        panel = ctk.CTkFrame(parent, border_width=2)
        panel.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(panel, text=title, font=self.fonts["bold"]).pack(pady=5)
        
        v = {
            "font_var": tk.StringVar(value=data["font"]), 
            "size_var": tk.StringVar(value=data["size"]),
            "color_var": tk.StringVar(value=data["color"]), 
            "bold_var": tk.IntVar(value=data["bold"]),
            "ml_var": tk.StringVar(value=data["ml"]), 
            "mr_var": tk.StringVar(value=data["mr"]), 
            "mv_var": tk.StringVar(value=data["mv"])
        }

        # 1. 预览区
        prev = tk.Label(panel, text=preview_text, font=("Arial", 12), bg="#2b2b2b", fg="white", pady=10)
        prev.pack(fill="x", padx=15, pady=5)

        # 辅助：ASS颜色转Hex
        def ass_to_hex(ass_color):
            try:
                import re
                m = re.search(r'&H[0-9A-F]{2}([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})', ass_color.upper())
                if m: return f"#{m.group(3)}{m.group(2)}{m.group(1)}"
            except: pass
            return "#FFFFFF"

        def sync(*_):
            try:
                sz = min(int(float(v["size_var"].get())), 24)
                wt = "bold" if v["bold_var"].get() else "normal"
                hex_c = ass_to_hex(v["color_var"].get())
                prev.config(fg=hex_c, font=(v["font_var"].get(), sz, wt))
                c_btn.config(bg=hex_c) # 同步更新色块背景
            except: pass

        # 2. 第一行：字体选择
        row1 = ctk.CTkFrame(panel, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=2)
        FontSelector(row1, v["font_var"], self.window)

        # 3. 第二行：大小、粗体、颜色色块
        row2 = ctk.CTkFrame(panel, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(row2, text="大小:").pack(side="left")
        ctk.CTkEntry(row2, textvariable=v["size_var"], width=45).pack(side="left", padx=5)
        ctk.CTkCheckBox(row2, text="B", variable=v["bold_var"], width=45).pack(side="left")
        
        # 纯色块按钮
        c_btn = tk.Label(row2, text="      ", relief="flat", cursor="hand2", width=8,
                         highlightthickness=1, highlightbackground="gray")
        c_btn.pack(side="right", padx=5)
        c_btn.bind("<Button-1>", lambda e: self._pick_color(v["color_var"], c_btn))

        # 4. 第三行：边距设置 (ML, MR, MV) - 确保这一段存在
        row3 = ctk.CTkFrame(panel, fg_color="transparent")
        row3.pack(fill="x", padx=15, pady=5)
        for label, var_name in [("L:", "ml_var"), ("R:", "mr_var"), ("V:", "mv_var")]:
            ctk.CTkLabel(row3, text=label, font=self.fonts["small"]).pack(side="left", padx=(2, 0))
            ctk.CTkEntry(row3, textvariable=v[var_name], width=40, height=24).pack(side="left", padx=2)

        # 监听变量变化
        for var in [v["font_var"], v["size_var"], v["bold_var"], v["color_var"]]:
            var.trace_add("write", sync)

        sync() # 初始刷新

        # 核心：必须挂载到 app 上，否则点击开始任务时拿不到这里的数值
        if title == "外语样式":
            self.app.kor_panel_ui = v
        else:
            self.app.chn_panel_ui = v

        return v

    def _pick_color(self, var, btn):
        color = colorchooser.askcolor(parent=self.window, initialcolor=btn.cget("bg"))
        if color[1]:
            rgb = color[0]
            var.set(f"&H00{int(rgb[2]):02X}{int(rgb[1]):02X}{int(rgb[0]):02X}&")
            btn.config(bg=color[1])