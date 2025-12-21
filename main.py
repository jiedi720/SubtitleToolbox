import win32com.client
import pythoncom
import os
import sys
import re
import threading
import configparser
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, colorchooser, font, messagebox, simpledialog

# ==========================================
# 资源路径获取
# ==========================================
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# ==========================================
# 模块搜索路径
# ==========================================
base_dir = os.path.dirname(os.path.abspath(__file__))
logic_dir = os.path.join(base_dir, 'logic')
if logic_dir not in sys.path:
    sys.path.append(logic_dir)

# ==========================================
# 导入模块
# ==========================================
try:
    import config
    # --- 修改点 1: 导入两个 TXT 函数 ---
    from logic.txt_logic import run_txt_merge_task, run_txt_creation_task
    from pdf_logic import run_pdf_task, run_pdf_merge_task
    from word_logic import run_word_creation_task, run_win32_merge_task
    from ass_logic import run_ass_task
except ImportError as e:
    messagebox.showerror("启动错误", f"无法加载核心模块！\n请确保已创建 'logic' 文件夹并将所有功能脚本放入其中。\n\n详细错误: {e}")
    sys.exit(1)

class UnifiedApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.root.title("Subtitle Toolbox")
        
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
            print(f"警告: 无法加载图标 - {e}")

        win_w, win_h = 700, 450 
        cx = int(self.root.winfo_screenwidth()/2 - win_w/2)
        cy = int(self.root.winfo_screenheight()/2 - win_h/2)
        self.root.geometry(f'{win_w}x{win_h}+{cx}+{cy}')
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.ui_font = ("Microsoft YaHei", 10)
        self.ui_font_bold = ("Microsoft YaHei", 10, "bold")
        self.ui_font_small = ("Microsoft YaHei", 9)

        config.init_fonts()

        self.default_kor_raw = "Style: KOR - Noto Serif KR,Noto Serif KR SemiBold,20,&H0026FCFF,&H000000FF,&H50000000,&H00000000,-1,0,0,0,100,100,0.1,0,1,0.6,0,2,10,10,34,1"
        self.default_chn_raw = "Style: CHN - Drama,小米兰亭,17,&H28FFFFFF,&H000000FF,&H64000000,&H00000000,-1,0,0,0,100,100,0,0,1,0.5,0,2,10,10,15,1"

        self.presets = self.load_presets()
        self.system_fonts = sorted(font.families())
        
        last_dir = self.load_last_directory()
        self.path_var = tk.StringVar(value=last_dir)
        
        self.current_preset_name = tk.StringVar(value="默认")
        self.task_mode = tk.StringVar(value="ASS")
        
        self.do_pdf = tk.BooleanVar(value=True)
        self.do_word = tk.BooleanVar(value=True)
        self.do_txt = tk.BooleanVar(value=True) 

        curr_data = self.presets.get("默认", {"kor": self.default_kor_raw, "chn": self.default_chn_raw})
        self.kor_parsed = self.parse_ass_style(curr_data["kor"])
        self.chn_parsed = self.parse_ass_style(curr_data["chn"])
        
        self.config_window = None
        self.kor_panel_ui = None
        self.chn_panel_ui = None

        self.setup_ui()
        self.root.deiconify()

    def setup_ui(self):
        global_frame = tk.LabelFrame(self.root, text="全局设置", font=self.ui_font, padx=10, pady=5)
        global_frame.pack(fill="x", padx=15, pady=5)

        path_frame = tk.Frame(global_frame)
        path_frame.pack(fill="x", pady=(0, 5))
        
        tk.Button(path_frame, text="📂", command=self.browse_folder, width=3, font=self.ui_font).pack(side="right", padx=5)
        tk.Button(path_frame, text="👀", command=self.open_current_folder, width=3, font=self.ui_font).pack(side="right", padx=(2,0))
        tk.Button(path_frame, text="👉", command=self.update_path_from_entry, width=3, font=self.ui_font).pack(side="right", padx=(5,0))
        
        self.path_entry = tk.Entry(path_frame, textvariable=self.path_var, font=self.ui_font)
        self.path_entry.pack(side="right", fill="x", expand=True, padx=5)
        self.path_entry.bind('<Return>', self.update_path_from_entry)

        tk.Label(path_frame, text="工作目录:", font=self.ui_font_bold).pack(side="right")

        opt_frame = tk.Frame(global_frame)
        opt_frame.pack(fill="x", pady=5)
        
        tk.Label(opt_frame, text="执行任务:", font=self.ui_font_bold).pack(side="left", padx=(0, 10))
        tk.Radiobutton(opt_frame, text="合并/转换字幕", variable=self.task_mode, value="ASS", font=self.ui_font).pack(side="left")
        tk.Radiobutton(opt_frame, text="生成台词剧本", variable=self.task_mode, value="PDF", font=self.ui_font).pack(side="left", padx=10)

        func_frame = tk.Frame(global_frame)
        func_frame.pack(fill="x", pady=5)

        tk.Label(func_frame, text="剧本格式:", font=self.ui_font_small).pack(side="left", padx=(0, 0))
        tk.Checkbutton(func_frame, text="TXT", variable=self.do_txt, font=self.ui_font_small).pack(side="left")
        tk.Checkbutton(func_frame, text="Word", variable=self.do_word, font=self.ui_font_small).pack(side="left", padx=5)
        tk.Checkbutton(func_frame, text="PDF", variable=self.do_pdf, font=self.ui_font_small).pack(side="left", padx=5)

        # --- 功能按钮区 ---
        tk.Button(func_frame, text="PDF合并", command=self.start_pdf_merge_thread, bg="#d93025", fg="white", font=self.ui_font_small).pack(side="right", padx=5)
        tk.Button(func_frame, text="Word合并", command=self.start_win32_thread, bg="#2b5797", fg="white", font=self.ui_font_small).pack(side="right", padx=5)
        tk.Button(func_frame, text="TXT合并", command=self.start_txt_merge_thread, bg="#fff9c4", font=self.ui_font_small).pack(side="right", padx=5)
        tk.Button(func_frame, text="🎨 ASS样式配置", command=self.open_ass_config_window, bg="#FF9800", font=self.ui_font_small).pack(side="right", padx=5)

        self.start_btn = tk.Button(self.root, text="开始处理", command=self.start_thread, bg="#0078d7", fg="white", font=self.ui_font_bold, width=20, height=1)
        self.start_btn.pack(pady=5, padx=20)
        
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=20, pady=5)
        
        self.log_area = scrolledtext.ScrolledText(self.root, height=10, font=("Consolas", 9), state='disabled', bg="#f8f9fa")
        self.log_area.pack(fill="both", padx=20, pady=5, expand=True)

    def open_ass_config_window(self):
        if self.config_window is not None and self.config_window.winfo_exists():
            self.config_window.lift()
            return

        self.config_window = tk.Toplevel(self.root)
        self.config_window.withdraw()
        self.config_window.title("ASS 字幕样式配置")
        try:
            icon_path = resource_path("subtitle-toolbox.ico")
            if os.path.exists(icon_path):
                self.config_window.iconbitmap(icon_path)
        except: pass
        
        self.config_window.geometry("900x250")
        
        win_w, win_h = 900, 250
        cx = int(self.root.winfo_screenwidth()/2 - win_w/2)
        cy = int(self.root.winfo_screenheight()/2 - win_h/2)
        self.config_window.geometry(f'{win_w}x{win_h}+{cx}+{cy}')

        preset_frame = tk.Frame(self.config_window, pady=10)
        preset_frame.pack(fill="x", padx=10)
        
        tk.Label(preset_frame, text="配置方案:", font=self.ui_font_bold).pack(side="left")
        self.preset_combo = ttk.Combobox(preset_frame, textvariable=self.current_preset_name, font=self.ui_font, width=15, state='readonly')
        self.preset_combo['values'] = list(self.presets.keys())
        self.preset_combo.pack(side="left", padx=5)
        self.preset_combo.bind("<<ComboboxSelected>>", self.on_preset_change)
        
        tk.Button(preset_frame, text="💾 保存新方案", command=self.save_preset_dialog, bg="#14d6f0", font=self.ui_font_small).pack(side="left", padx=5)
        tk.Button(preset_frame, text="❌ 删除方案", command=self.delete_preset, bg="#ef090d", fg="white", font=self.ui_font_small).pack(side="left", padx=5)
        tk.Button(preset_frame, text="📝 打开配置文件", command=self.open_config_file, bg="#FEE60A", font=self.ui_font_small).pack(side="left", padx=5)

        panels_frame = tk.Frame(self.config_window)
        panels_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.kor_panel_ui = self.create_style_panel(panels_frame, "外语样式", self.kor_parsed, "안녕하세요 こんにちは Hello")
        self.chn_panel_ui = self.create_style_panel(panels_frame, "中文样式", self.chn_parsed, "你好世界 Hello")
        
        self.config_window.deiconify()

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, str(message) + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def browse_folder(self):
        current_path = self.path_var.get().strip()
        initial_dir = current_path if os.path.isdir(current_path) else None
        d = filedialog.askdirectory(initialdir=initial_dir)
        if d: self.path_var.set(d)

    def open_current_folder(self):
        p = self.path_var.get().strip()
        if os.path.isdir(p):
            try: 
                os.startfile(p)
                self.log(f"📂 已打开文件夹: {p}")
            except Exception as e: self.log(f"❌ 打开失败: {e}")
        else: messagebox.showwarning("错误", "目录不存在！")

    def update_path_from_entry(self, event=None):
        p = self.path_var.get().strip()
        if os.path.isdir(p):
            self.log(f"📂 目录已更新: {p}")
            self.path_entry.config(bg="#d4edda")
            self.root.after(500, lambda: self.path_entry.config(bg="white"))
        else:
            self.log(f"⚠️ 路径不存在: {p}")
            messagebox.showwarning("路径错误", "输入的目录不存在！")
            self.path_entry.config(bg="#f8d7da")
            self.root.after(500, lambda: self.path_entry.config(bg="white"))

    def load_last_directory(self):
        fallback = r"H:\剧集\韩剧"
        if os.path.exists(config.CONFIG_FILE):
            try:
                c = configparser.ConfigParser(); c.read(config.CONFIG_FILE, encoding="utf-8")
                if c.has_option("General", "last_dir"): return c.get("General", "last_dir")
            except: pass
        return fallback

    def load_presets(self):
        default = {"默认": {"kor": self.default_kor_raw, "chn": self.default_chn_raw}}
        if os.path.exists(config.CONFIG_FILE):
            try:
                c = configparser.ConfigParser(); c.read(config.CONFIG_FILE, encoding="utf-8")
                if c.sections(): 
                    return {s: {"kor": c.get(s, "kor"), "chn": c.get(s, "chn")} for s in c.sections() if s != "General"}
            except: pass
        return default

    def on_close(self):
        try:
            c = configparser.ConfigParser()
            if os.path.exists(config.CONFIG_FILE): c.read(config.CONFIG_FILE, encoding="utf-8")
            if not c.has_section("General"): c.add_section("General")
            c.set("General", "last_dir", self.path_var.get().strip())
            with open(config.CONFIG_FILE, "w", encoding="utf-8") as f: c.write(f)
        except Exception as e: print(f"保存设置失败: {e}")
        finally: self.root.destroy()

    def save_presets_to_file(self):
        try:
            c = configparser.ConfigParser()
            if os.path.exists(config.CONFIG_FILE): c.read(config.CONFIG_FILE, encoding="utf-8")
            for name, styles in self.presets.items():
                if not c.has_section(name): c.add_section(name)
                c.set(name, "kor", styles["kor"])
                c.set(name, "chn", styles["chn"])
            with open(config.CONFIG_FILE, "w", encoding="utf-8") as f: c.write(f)
        except Exception as e: messagebox.showerror("错误", str(e))

    def open_config_file(self):
        if not os.path.exists(config.CONFIG_FILE): self.save_presets_to_file()
        try: os.startfile(config.CONFIG_FILE)
        except Exception as e: messagebox.showerror("错误", str(e))

    def on_preset_change(self, event):
        name = self.current_preset_name.get()
        if name in self.presets:
            d = self.presets[name]
            self.kor_parsed = self.parse_ass_style(d["kor"])
            self.chn_parsed = self.parse_ass_style(d["chn"])
            if self.config_window is not None and self.config_window.winfo_exists():
                self.update_panel_ui(self.kor_panel_ui, self.kor_parsed)
                self.update_panel_ui(self.chn_panel_ui, self.chn_parsed)

    def parse_ass_style(self, style_line):
        if "Style:" not in style_line: return self.parse_ass_style(self.default_kor_raw)
        parts = style_line.replace("Style:", "").strip().split(',')
        while len(parts) < 23: parts.append("0")
        return {"font": parts[1].strip(), "size": parts[2].strip(), "color": parts[3].strip(), 
                "bold": 1 if parts[7].strip() == "-1" else 0, "ml": parts[19].strip(), 
                "mr": parts[20].strip(), "mv": parts[21].strip(), "raw": style_line.strip()}

    def construct_style_line(self, original_raw, ui, style_name):
        parts = original_raw.replace("Style:", "").strip().split(',')
        while len(parts) < 23: parts.append("0")
        
        if ui:
            parts[0] = style_name
            parts[1] = ui["font_var"].get()
            parts[2] = ui["size_var"].get()
            parts[3] = ui["color_var"].get()
            parts[7] = "-1" if ui["bold_var"].get() else "0"
            parts[19] = ui["ml_var"].get()
            parts[20] = ui["mr_var"].get()
            parts[21] = ui["mv_var"].get()
        else:
            data = self.kor_parsed if "KOR" in style_name else self.chn_parsed
            parts[0] = style_name
            parts[1] = data["font"]
            parts[2] = data["size"]
            parts[3] = data["color"]
            parts[7] = "-1" if data["bold"] else "0"
            parts[19] = data["ml"]
            parts[20] = data["mr"]
            parts[21] = data["mv"]

        return "Style: " + ",".join(parts)

    def save_preset_dialog(self):
        n = simpledialog.askstring("保存方案", "请输入名称:", initialvalue=self.current_preset_name.get())
        if n:
            l_k = self.construct_style_line(self.kor_parsed["raw"], self.kor_panel_ui, "KOR")
            l_c = self.construct_style_line(self.chn_parsed["raw"], self.chn_panel_ui, "CHN")
            self.presets[n.strip()] = {"kor": l_k, "chn": l_c}
            self.save_presets_to_file()
            self.preset_combo['values'] = list(self.presets.keys())
            self.preset_combo.set(n.strip())

    def delete_preset(self):
        n = self.current_preset_name.get()
        if n != "默认" and messagebox.askyesno("删除", f"确定删除 [{n}] 吗？"):
            del self.presets[n]
            self.save_presets_to_file()
            self.current_preset_name.set("默认")
            self.preset_combo['values'] = list(self.presets.keys())
            self.on_preset_change(None)

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
            if isinstance(v, tk.StringVar) or isinstance(v, tk.IntVar):
                v.trace_add("write", update_data)

        f_row = tk.Frame(panel); f_row.pack(fill="x", pady=2)
        tk.Label(f_row, text="字体:", font=self.ui_font, width=4, anchor="w").pack(side="left")
        
        combo = ttk.Combobox(f_row, textvariable=vars["font_var"], values=self.system_fonts, state="readonly", font=self.ui_font)
        combo.pack(side="left", fill="x", expand=True)
        
        p_label = tk.Label(panel, text=preview_text, font=("Arial", 10), bg="white", relief="sunken", height=1)
        p_label.pack(fill="x", pady=(2, 8))
        
        def update_p(*args):
            try: 
                f, sz = vars["font_var"].get(), int(float(vars["size_var"].get()))
                w = "bold" if vars["bold_var"].get() else "normal"
                p_label.config(font=(f, min(sz, 28), w))
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

    def update_panel_ui(self, ui, data):
        if ui:
            ui["font_var"].set(data["font"]); ui["size_var"].set(data["size"]); ui["color_var"].set(data["color"])
            ui["ml_var"].set(data["ml"]); ui["mr_var"].set(data["mr"]); ui["mv_var"].set(data["mv"]); ui["bold_var"].set(data["bold"])
            self.sync_color(ui["color_var"], ui["c_btn"]); ui["update_func"]()

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

    def start_thread(self): 
        threading.Thread(target=self.process, daemon=True).start()

    def start_win32_thread(self):
        target_dir = self.path_var.get().strip()
        if not target_dir or not os.path.exists(target_dir):
            messagebox.showerror("错误", "无效的目录")
            return
        threading.Thread(target=run_win32_merge_task, args=(target_dir, self.log, self.progress, self.root), daemon=True).start()

    def start_pdf_merge_thread(self):
        target_dir = self.path_var.get().strip()
        if not target_dir or not os.path.exists(target_dir):
            messagebox.showerror("错误", "无效的目录")
            return
        threading.Thread(target=run_pdf_merge_task, args=(target_dir, self.log, self.progress, self.root), daemon=True).start()

    def start_txt_merge_thread(self):
        target_dir = self.path_var.get().strip()
        if not target_dir or not os.path.exists(target_dir):
            messagebox.showerror("错误", "无效的目录")
            return
        threading.Thread(target=run_txt_merge_task, args=(target_dir, self.log, self.progress, self.root), daemon=True).start()

    def process(self):
        target_dir = self.path_var.get().strip()
        if not target_dir or not os.path.exists(target_dir): 
            messagebox.showerror("错误", "无效的目录")
            return
            
        self.start_btn.config(state='disabled')
        self.log(f"--- 任务启动: {target_dir} ---")
        
        try:
            mode = self.task_mode.get()
            if mode == "ASS":
                style_kor = self.construct_style_line(self.kor_parsed["raw"], self.kor_panel_ui, "KOR - Noto Serif KR")
                style_chn = self.construct_style_line(self.chn_parsed["raw"], self.chn_panel_ui, "CHN - Drama")
                run_ass_task(target_dir, {"kor": style_kor, "chn": style_chn}, self.log, self.progress, self.root)
                
            elif mode == "PDF":
                if not self.do_pdf.get() and not self.do_word.get() and not self.do_txt.get():
                    self.log("⚠️ 未勾选任何导出格式。")
                else:
                    if self.do_pdf.get(): 
                        run_pdf_task(target_dir, self.log, self.progress, self.root)
                    if self.do_word.get(): 
                        run_word_creation_task(target_dir, self.log, self.progress, self.root)
                    if self.do_txt.get(): 
                        # --- 修改点 2: 勾选 TXT 时，调用 SRT->TXT 生成函数 ---
                        run_txt_creation_task(target_dir, self.log, self.progress, self.root)
                        
            self.log("✅ 任务完成！")
        except Exception as e:
            self.log(f"❌ 严重错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.start_btn.config(state='normal')
            self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedApp(root)
    root.mainloop()