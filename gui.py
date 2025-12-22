import os
import sys
import re
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, colorchooser, messagebox, simpledialog, font

# 资源路径获取
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class ToolboxGUI:
    def __init__(self, root, controller):
        """
        :param root: tk.Tk() 实例
        :param controller: UnifiedApp 实例
        """
        self.root = root
        self.app = controller 
        
        # 字体设置
        self.ui_font = ("Microsoft YaHei", 10)
        self.ui_font_bold = ("Microsoft YaHei", 10, "bold")
        self.ui_font_small = ("Microsoft YaHei", 9)
        self.system_fonts = sorted(font.families()) if 'font' in globals() else []

        self.config_window = None
        self.kor_panel_ui = None
        self.chn_panel_ui = None

        self._init_icon()
        self.setup_main_window()

    def _init_icon(self):
        icon_name = "subtitle-toolbox.ico"
        try:
            icon_path = resource_path(icon_name)
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                parent_icon = os.path.join(os.path.dirname(os.path.dirname(icon_path)), icon_name)
                if os.path.exists(parent_icon):
                     self.root.iconbitmap(parent_icon)
        except Exception as e:
            print(f"图标加载警告: {e}")

    def setup_main_window(self):
        global_frame = tk.LabelFrame(self.root, text="全局设置", font=self.ui_font, padx=10, pady=5)
        global_frame.pack(fill="x", padx=15, pady=5)

        # 1. 输入路径
        in_frame = tk.Frame(global_frame)
        in_frame.pack(fill="x", pady=(0, 5))
        
        # 右侧按钮群
        tk.Button(in_frame, text="📂", command=self.app.browse_folder, width=3, font=self.ui_font).pack(side="right", padx=5)
        tk.Button(in_frame, text="👀", command=self.app.open_current_folder, width=3, font=self.ui_font).pack(side="right", padx=(2,0))
        
        # 确认按钮 👉 (手动触发更新)
        tk.Button(in_frame, text="👉", command=lambda: self.update_path_from_entry(self.app.path_var, self.app.path_entry), width=3, font=self.ui_font).pack(side="right", padx=(5,0))
        
        # 输入框
        self.app.path_entry = tk.Entry(in_frame, textvariable=self.app.path_var, font=self.ui_font)
        self.app.path_entry.pack(side="right", fill="x", expand=True, padx=5)
        self.app.path_entry.bind('<Return>', lambda e: self.update_path_from_entry(self.app.path_var, self.app.path_entry))
        tk.Label(in_frame, text="源文件目录:", font=self.ui_font_bold, width=10, anchor="e").pack(side="right")

        # 2. 输出路径
        out_frame = tk.Frame(global_frame)
        out_frame.pack(fill="x", pady=(0, 5))
        
        tk.Button(out_frame, text="📂", command=self.app.browse_output_folder, width=3, font=self.ui_font).pack(side="right", padx=5)
        tk.Button(out_frame, text="👀", command=self.app.open_output_folder, width=3, font=self.ui_font).pack(side="right", padx=(2,0))
        
        # 确认按钮 👉
        tk.Button(out_frame, text="👉", command=lambda: self.update_path_from_entry(self.app.output_path_var, self.app.out_entry), width=3, font=self.ui_font).pack(side="right", padx=(5,0))
        
        self.app.out_entry = tk.Entry(out_frame, textvariable=self.app.output_path_var, font=self.ui_font, fg="#0056b3")
        self.app.out_entry.pack(side="right", fill="x", expand=True, padx=5)
        self.app.out_entry.bind('<Return>', lambda e: self.update_path_from_entry(self.app.output_path_var, self.app.out_entry))
        tk.Label(out_frame, text="输出位置:", font=self.ui_font_bold, width=10, anchor="e").pack(side="right")
        
        tk.Label(global_frame, text="(留空则默认在源目录下生成script文件夹)", font=("Arial", 8), fg="gray").pack(anchor="w", padx=90)

        # 3. 任务模式
        opt_frame = tk.Frame(global_frame)
        opt_frame.pack(fill="x", pady=5)
        tk.Label(opt_frame, text="执行任务:", font=self.ui_font_bold).pack(side="left", padx=(0, 10))
        tk.Radiobutton(opt_frame, text="合并/转换字幕", variable=self.app.task_mode, value="ASS", font=self.ui_font).pack(side="left")
        tk.Radiobutton(opt_frame, text="生成台词剧本", variable=self.app.task_mode, value="PDF", font=self.ui_font).pack(side="left", padx=10)

        # 4. 分组
        group_frame = tk.Frame(global_frame)
        group_frame.pack(fill="x", pady=2)
        tk.Checkbutton(group_frame, text="启用智能分卷(3-4集/卷)", variable=self.app.enable_grouping, font=self.ui_font_small).pack(side="left")
        
        # 5. 格式与功能区
        func_frame = tk.Frame(global_frame)
        func_frame.pack(fill="x", pady=5)
        tk.Label(func_frame, text="剧本格式:", font=self.ui_font_small).pack(side="left", padx=(0, 0))
        tk.Checkbutton(func_frame, text="TXT", variable=self.app.do_txt, font=self.ui_font_small).pack(side="left")
        tk.Checkbutton(func_frame, text="Word", variable=self.app.do_word, font=self.ui_font_small).pack(side="left", padx=5)
        tk.Checkbutton(func_frame, text="PDF", variable=self.app.do_pdf, font=self.ui_font_small).pack(side="left", padx=5)

        tk.Button(func_frame, text="🎨 ASS样式", command=self.open_ass_config_window, bg="#FF9800", font=self.ui_font_small).pack(side="right", padx=5)
        
        # 6. 底部合并区 & 清空
        merge_frame = tk.Frame(global_frame)
        merge_frame.pack(fill="x", pady=2)
        
        tk.Button(merge_frame, text="❌ 清空输出目录", command=self.app.clear_output_folder, bg="#795548", fg="white", font=self.ui_font_small).pack(side="right", padx=5)
        tk.Button(merge_frame, text="PDF合并", command=self.app.start_pdf_merge_thread, bg="#d93025", fg="white", font=self.ui_font_small).pack(side="right", padx=5)
        tk.Button(merge_frame, text="Word合并", command=self.app.start_win32_thread, bg="#2b5797", fg="white", font=self.ui_font_small).pack(side="right", padx=5)
        tk.Button(merge_frame, text="TXT合并", command=self.app.start_txt_merge_thread, bg="#fff9c4", font=self.ui_font_small).pack(side="right", padx=5)

        self.app.start_btn = tk.Button(self.root, text="开始处理", command=self.app.start_thread, bg="#0078d7", fg="white", font=self.ui_font_bold, width=20, height=1)
        self.app.start_btn.pack(pady=5, padx=20)
        
        self.app.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.app.progress.pack(fill="x", padx=20, pady=5)
        
        self.app.log_area = scrolledtext.ScrolledText(self.root, height=10, font=("Consolas", 9), state='disabled', bg="#f8f9fa")
        self.app.log_area.pack(fill="both", padx=20, pady=5, expand=True)

    # ==========================================
    # [补回] 缺失的辅助方法
    # ==========================================
    def update_path_from_entry(self, var, entry_widget):
        p = var.get().strip()
        if os.path.isdir(p):
            self.app.log(f"📂 路径有效: {p}")
            entry_widget.config(bg="#d4edda")
            self.root.after(500, lambda: entry_widget.config(bg="white"))
        else:
            if p == "" and var == self.app.output_path_var:
                return
            self.app.log(f"⚠️ 路径不存在: {p}")
            entry_widget.config(bg="#f8d7da")
            self.root.after(500, lambda: entry_widget.config(bg="white"))

    def open_folder(self, p):
        if os.path.isdir(p):
            try: 
                os.startfile(p)
                self.app.log(f"📂 打开: {p}")
            except Exception as e: 
                self.app.log(f"❌ 无法打开: {e}")
        else: 
            messagebox.showwarning("错误", f"目录不存在:\n{p}")

    def open_output_folder(self):
        target = self.app.get_output_dir()
        if not os.path.exists(target):
            try: 
                os.makedirs(target)
                self.app.log(f"创建输出目录: {target}")
            except: pass
        self.open_folder(target)

    # ==========================================
    # ASS 配置窗口 (保持不变)
    # ==========================================
    def open_ass_config_window(self):
        if self.config_window is not None and self.config_window.winfo_exists():
            self.config_window.lift(); return
        self.config_window = tk.Toplevel(self.root); self.config_window.withdraw()
        self.config_window.title("ASS字幕样式")
        try:
            if os.path.exists(resource_path("subtitle-toolbox.ico")): self.config_window.iconbitmap(resource_path("subtitle-toolbox.ico"))
        except: pass
        
        win_w, win_h = 900, 250
        cx = int(self.root.winfo_screenwidth()/2 - win_w/2)
        cy = int(self.root.winfo_screenheight()/2 - win_h/2)
        self.config_window.geometry(f'{win_w}x{win_h}+{cx}+{cy}')

        preset_frame = tk.Frame(self.config_window, pady=10); preset_frame.pack(fill="x", padx=10)
        tk.Label(preset_frame, text="配置方案:", font=self.ui_font_bold).pack(side="left")
        
        self.app.preset_combo = ttk.Combobox(preset_frame, textvariable=self.app.current_preset_name, font=self.ui_font, width=15, state='readonly')
        self.app.preset_combo['values'] = list(self.app.presets.keys()); self.app.preset_combo.pack(side="left", padx=5)
        self.app.preset_combo.bind("<<ComboboxSelected>>", self.app.on_preset_change)
        
        tk.Button(preset_frame, text="💾 保存新方案", command=self.app.save_preset_dialog, bg="#14d6f0", font=self.ui_font_small).pack(side="left", padx=5)
        tk.Button(preset_frame, text="❌ 删除方案", command=self.app.delete_preset, bg="#ef090d", fg="white", font=self.ui_font_small).pack(side="left", padx=5)
        tk.Button(preset_frame, text="📝 打开配置文件", command=self.app.open_config_file, bg="#FEE60A", font=self.ui_font_small).pack(side="left", padx=5)

        panels_frame = tk.Frame(self.config_window); panels_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.kor_panel_ui = self.create_style_panel(panels_frame, "外语样式", self.app.kor_parsed, "안녕하세요 こんにちは Hello")
        self.chn_panel_ui = self.create_style_panel(panels_frame, "中文样式", self.app.chn_parsed, "你好世界 Hello")
        
        self.app.kor_panel_ui = self.kor_panel_ui
        self.app.chn_panel_ui = self.chn_panel_ui
        
        self.config_window.deiconify()

    def create_style_panel(self, parent, title, initial_data, preview_text):
        panel = tk.LabelFrame(parent, text=title, font=self.ui_font, padx=10, pady=5)
        panel.pack(side="left", fill="both", expand=True, padx=8)
        
        vars = {
            "font_var": tk.StringVar(value=initial_data["font"]), 
            "size_var": tk.StringVar(value=initial_data["size"]), 
            "color_var": tk.StringVar(value=initial_data["color"]), 
            "ml_var": tk.StringVar(value=initial_data["ml"]), 
            "mr_var": tk.StringVar(value=initial_data["mr"]), 
            "mv_var": tk.StringVar(value=initial_data["mv"]), 
            "bold_var": tk.IntVar(value=initial_data["bold"])
        }
        
        def update_data(*args):
            initial_data["font"] = vars["font_var"].get()
            initial_data["size"] = vars["size_var"].get()
            initial_data["color"] = vars["color_var"].get()
            initial_data["ml"] = vars["ml_var"].get()
            initial_data["mr"] = vars["mr_var"].get()
            initial_data["mv"] = vars["mv_var"].get()
            initial_data["bold"] = vars["bold_var"].get()
            
        for v in vars.values():
            if isinstance(v, (tk.StringVar, tk.IntVar)): v.trace_add("write", update_data)

        f_row = tk.Frame(panel); f_row.pack(fill="x", pady=2)
        tk.Label(f_row, text="字体:", font=self.ui_font, width=4, anchor="w").pack(side="left")
        
        try: from tkinter import font; fonts = sorted(font.families())
        except: fonts = []
        
        combo = ttk.Combobox(f_row, textvariable=vars["font_var"], values=fonts, state="readonly", font=self.ui_font)
        combo.pack(side="left", fill="x", expand=True)
        
        p_label = tk.Label(panel, text=preview_text, font=("Arial", 10), bg="white", relief="sunken", height=1)
        p_label.pack(fill="x", pady=(2, 8))
        
        def update_p(*args):
            try: p_label.config(font=(vars["font_var"].get(), min(int(float(vars["size_var"].get())), 28), "bold" if vars["bold_var"].get() else "normal"))
            except: pass
        combo.bind("<<ComboboxSelected>>", update_p)
        
        param_row = tk.Frame(panel); param_row.pack(fill="x", pady=2)
        left = tk.Frame(param_row); left.pack(side="left")
        tk.Label(left, text="号:", font=self.ui_font).pack(side="left")
        tk.Spinbox(left, from_=1, to=200, textvariable=vars["size_var"], width=3, font=self.ui_font, command=update_p).pack(side="left", padx=(0,5))
        tk.Checkbutton(left, text="B", variable=vars["bold_var"], font=("Georgia", 10, "bold"), command=update_p).pack(side="left", padx=(0,5))
        
        c_btn = tk.Label(left, width=2, relief="ridge", borderwidth=1)
        c_btn.pack(side="left", padx=(2,2), fill="y")
        c_btn.bind("<Button-1>", lambda e: self.pick_color(vars["color_var"], c_btn))
        
        tk.Entry(left, textvariable=vars["color_var"], font=self.ui_font_small, width=11).pack(side="left")
        self.sync_color(vars["color_var"], c_btn)
        
        tk.Label(param_row, text="").pack(side="left", expand=True)
        right = tk.Frame(param_row); right.pack(side="right")
        
        def qs(txt, v): 
            tk.Label(right, text=txt, font=self.ui_font_small).pack(side="left", padx=(3,0))
            tk.Spinbox(right, from_=0, to=500, textvariable=v, width=3, font=self.ui_font).pack(side="left")
        qs("L:", vars["ml_var"]); qs("R:", vars["mr_var"]); qs("V:", vars["mv_var"])
        
        update_p()
        vars.update({"c_btn": c_btn, "update_func": update_p})
        return vars

    def sync_color(self, var, btn):
        m = re.search(r'&H[0-9A-F]{2}([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})', var.get().upper())
        if m: btn.config(bg=f"#{m.groups()[2]}{m.groups()[1]}{m.groups()[0]}")

    def pick_color(self, var, btn):
        code = colorchooser.askcolor()
        if code[1]:
            rgb = code[0]
            m = re.search(r'&H([0-9A-F]{2})', var.get().upper())
            alpha = m.group(1) if m else "00"
            var.set(f"&H{alpha}{int(rgb[2]):02X}{int(rgb[1]):02X}{int(rgb[0]):02X}&")
            btn.config(bg=code[1])

    def update_panel_ui(self, ui, data):
        if ui:
            ui["font_var"].set(data["font"]); ui["size_var"].set(data["size"]); ui["color_var"].set(data["color"])
            ui["ml_var"].set(data["ml"]); ui["mr_var"].set(data["mr"]); ui["mv_var"].set(data["mv"]); ui["bold_var"].set(data["bold"])
            self.sync_color(ui["color_var"], ui["c_btn"]); ui["update_func"]()