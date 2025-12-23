import win32com.client
import pythoncom
import os
import sys
import re
import threading
import configparser
import tkinter as tk
import argparse 
# [修复] 增加 filedialog 引用，解决 NameError
from tkinter import messagebox, simpledialog, filedialog

# 导入 GUI 模块
from gui import ToolboxGUI 

try:
    from send2trash import send2trash
    HAS_SEND2TRASH = True
except ImportError:
    HAS_SEND2TRASH = False

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir) 
logic_dir = os.path.join(base_dir, 'logic')
if logic_dir not in sys.path:
    sys.path.append(logic_dir)

try:
    import config
    from logic.txt_logic import run_txt_merge_task, run_txt_creation_task
    from logic.pdf_logic import run_pdf_task, run_pdf_merge_task
    from logic.word_logic import run_word_creation_task, run_win32_merge_task
    from logic.ass_logic import run_ass_task
except ImportError as e:
    print(f"警告: 核心模块导入失败 - {e}")
    def run_txt_merge_task(*args, **kwargs): pass
    def run_txt_creation_task(*args, **kwargs): pass
    def run_pdf_task(*args, **kwargs): pass
    def run_pdf_merge_task(*args, **kwargs): pass
    def run_word_creation_task(*args, **kwargs): pass
    def run_win32_merge_task(*args, **kwargs): pass
    def run_ass_task(*args, **kwargs): pass

class UnifiedApp:
    def __init__(self, root, startup_path=None, startup_out=None):
        self.root = root
        self.startup_path = startup_path
        self.startup_out = startup_out 

        self.root.withdraw()
        self.root.title("Subtitle Toolbox")
        
        win_w, win_h = 700, 520
        cx = int(self.root.winfo_screenwidth()/2 - win_w/2)
        cy = int(self.root.winfo_screenheight()/2 - win_h/2)
        self.root.geometry(f'{win_w}x{win_h}+{cx}+{cy}')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        try: config.init_fonts()
        except: pass

        self.default_kor_raw = "Style: KOR - Noto Serif KR,Noto Serif KR SemiBold,20,&H0026FCFF,&H000000FF,&H50000000,&H00000000,-1,0,0,0,100,100,0.1,0,1,0.6,0,2,10,10,34,1"
        self.default_chn_raw = "Style: CHN - Drama,小米兰亭,17,&H28FFFFFF,&H000000FF,&H64000000,&H00000000,-1,0,0,0,100,100,0,0,1,0.5,0,2,10,10,15,1"

        self.presets = self.load_presets()
        
        self.path_var = tk.StringVar()         
        self.output_path_var = tk.StringVar()  
        self.current_preset_name = tk.StringVar(value="默认")
        self.task_mode = tk.StringVar(value="ASS")
        
        self.do_pdf = tk.BooleanVar(value=True)
        self.do_word = tk.BooleanVar(value=True)
        self.do_txt = tk.BooleanVar(value=True) 
        self.enable_grouping = tk.BooleanVar(value=False)

        self.load_settings()

        curr_data = self.presets.get("默认", {"kor": self.default_kor_raw, "chn": self.default_chn_raw})
        self.kor_parsed = self.parse_ass_style(curr_data["kor"])
        self.chn_parsed = self.parse_ass_style(curr_data["chn"])
        
        self.gui = ToolboxGUI(self.root, self)
        
        self.root.deiconify()

    def on_close(self):
        self.save_settings()
        self.root.destroy()

    def get_output_dir(self):
        custom_out = self.output_path_var.get().strip()
        if custom_out: return custom_out
        source_dir = self.path_var.get().strip()
        if source_dir: return os.path.join(source_dir, "script")
        return ""

    def clear_output_folder(self):
        if not HAS_SEND2TRASH:
            messagebox.showerror("缺少组件", "需要安装 send2trash 库。\npip install send2trash")
            return
        target_out = self.get_output_dir()
        if not target_out or not os.path.exists(target_out):
            messagebox.showinfo("提示", "输出目录不存在。")
            return
        try: items = os.listdir(target_out)
        except Exception as e: messagebox.showerror("错误", f"无法读取: {e}"); return
        if not items: messagebox.showinfo("提示", "目录已空。"); return
        if not messagebox.askyesno("确认删除", f"路径: {target_out}\n\n即将清空该目录 (含子文件夹)。\n确定吗？"): return
        deleted_count = 0; error_count = 0
        for item in items:
            full_path = os.path.join(target_out, item)
            try: send2trash(full_path); deleted_count += 1
            except Exception as e: print(f"删除失败: {e}"); error_count += 1
        msg = f"✅ 已清理: {deleted_count} 个项目"; 
        if error_count > 0: msg += f" (失败 {error_count})"
        self.log(f"[清理] {msg}")

    def start_thread(self): 
        threading.Thread(target=self.process, daemon=True).start()
    def start_win32_thread(self): self.start_generic_task(run_win32_merge_task)
    def start_pdf_merge_thread(self): self.start_generic_task(run_pdf_merge_task)
    def start_txt_merge_thread(self): self.start_generic_task(run_txt_merge_task)
    
# ==========================================
    # 逻辑操作：多线程任务
    # ==========================================
    def start_generic_task(self, task_func):
        target_dir = self.path_var.get().strip()
        if not target_dir or not os.path.exists(target_dir): 
            messagebox.showerror("错误", "无效的目录")
            return
            
        # 【彻底修复点】获取路径，但绝对不要在这里调用 os.makedirs
        # 合并任务（Merge Task）将直接使用 target_dir 去找子文件夹
        # 生成任务（Creation Task）则由其内部逻辑在需要时才创建目录
        final_output_dir = self.get_output_dir()
        
        threading.Thread(
            target=task_func, 
            args=(target_dir, self.log, self.progress, self.root), 
            kwargs={'output_dir': final_output_dir}, 
            daemon=True
        ).start()

    def process(self):
        target_dir = self.path_var.get().strip()
        if not target_dir or not os.path.exists(target_dir): messagebox.showerror("错误", "无效的目录"); return
        final_output_dir = self.get_output_dir()
        if not os.path.exists(final_output_dir): 
            try: os.makedirs(final_output_dir)
            except Exception as e: self.log(f"❌ 无法创建输出目录: {e}"); return
        
        self.start_btn.config(state='disabled'); self.log(f"--- 任务启动 ---"); self.log(f"源目录: {target_dir}"); self.log(f"输出至: {final_output_dir}")
        batch_n = 4 if self.enable_grouping.get() else 0
        try:
            mode = self.task_mode.get()
            if mode == "ASS":
                run_ass_task(target_dir, {"kor": self.gui.construct_style_line(self.kor_parsed["raw"], self.gui.kor_panel_ui, "KOR"), "chn": self.gui.construct_style_line(self.chn_parsed["raw"], self.gui.chn_panel_ui, "CHN")}, self.log, self.progress, self.root, output_dir=final_output_dir)
            elif mode == "PDF":
                if not self.do_pdf.get() and not self.do_word.get() and not self.do_txt.get(): self.log("⚠️ 未勾选任何导出格式。")
                else:
                    if self.do_pdf.get(): run_pdf_task(target_dir, self.log, self.progress, self.root, batch_size=batch_n, output_dir=final_output_dir)
                    if self.do_word.get(): run_word_creation_task(target_dir, self.log, self.progress, self.root, batch_size=batch_n, output_dir=final_output_dir)
                    if self.do_txt.get(): run_txt_creation_task(target_dir, self.log, self.progress, self.root, batch_size=batch_n, output_dir=final_output_dir)
            self.log("✅ 任务完成！")
        except Exception as e: self.log(f"❌ 严重错误: {e}"); import traceback; traceback.print_exc()
        finally: self.start_btn.config(state='normal'); self.progress["value"] = 0

    def browse_folder(self):
        d = filedialog.askdirectory(initialdir=self.path_var.get().strip() or None)
        if d: self.path_var.set(d)
    def browse_output_folder(self):
        d = filedialog.askdirectory(initialdir=self.output_path_var.get().strip() or self.path_var.get().strip() or None)
        if d: self.output_path_var.set(d)
    def open_current_folder(self): self.gui.open_folder(self.path_var.get().strip())
    def open_output_folder(self): self.gui.open_output_folder()
    
    def update_path_from_entry(self, var, entry_widget):
        self.gui.update_path_from_entry(var, entry_widget)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, str(message) + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def load_presets(self):
        default = {"默认": {"kor": self.default_kor_raw, "chn": self.default_chn_raw}}
        try:
            c = configparser.ConfigParser(); c.read(config.CONFIG_FILE, encoding="utf-8")
            if c.sections(): return {s: {"kor": c.get(s, "kor"), "chn": c.get(s, "chn")} for s in c.sections() if s != "General"}
        except: pass
        return default

    def save_presets_to_file(self):
        try:
            c = configparser.ConfigParser()
            if os.path.exists(config.CONFIG_FILE): c.read(config.CONFIG_FILE, encoding="utf-8")
            for name, styles in self.presets.items():
                if not c.has_section(name): c.add_section(name)
                c.set(name, "kor", styles["kor"]); c.set(name, "chn", styles["chn"])
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
            if self.gui.config_window and self.gui.config_window.winfo_exists():
                self.gui.update_panel_ui(self.gui.kor_panel_ui, self.kor_parsed)
                self.gui.update_panel_ui(self.gui.chn_panel_ui, self.chn_parsed)

    def parse_ass_style(self, style_line):
        parts = style_line.replace("Style:", "").strip().split(',')
        while len(parts) < 23: parts.append("0")
        return {"font": parts[1].strip(), "size": parts[2].strip(), "color": parts[3].strip(), "bold": 1 if parts[7].strip()=="-1" else 0, "ml": parts[19].strip(), "mr": parts[20].strip(), "mv": parts[21].strip(), "raw": style_line.strip()}

    def save_preset_dialog(self):
        n = simpledialog.askstring("保存", "方案名称:", initialvalue=self.current_preset_name.get())
        if n:
            l_k = self.gui.construct_style_line(self.kor_parsed["raw"], self.gui.kor_panel_ui, "KOR")
            l_c = self.gui.construct_style_line(self.chn_parsed["raw"], self.gui.chn_panel_ui, "CHN")
            self.presets[n.strip()] = {"kor": l_k, "chn": l_c}
            self.save_presets_to_file()
            self.gui.preset_combo['values'] = list(self.presets.keys())
            self.gui.preset_combo.set(n.strip())

    def delete_preset(self):
        n = self.current_preset_name.get()
        if n != "默认" and messagebox.askyesno("删除", f"确定删除 [{n}] 吗？"):
            del self.presets[n]; self.save_presets_to_file()
            self.current_preset_name.set("默认")
            self.gui.preset_combo['values'] = list(self.presets.keys())
            self.on_preset_change(None)

    def load_settings(self):
        fallback_dir = "C:/"
        final_path = fallback_dir
        if os.path.exists(config.CONFIG_FILE):
            try:
                c = configparser.ConfigParser(); c.read(config.CONFIG_FILE, encoding="utf-8")
                if c.has_section("General"):
                    if c.has_option("General", "last_dir"): final_path = c.get("General", "last_dir")
                    if c.has_option("General", "custom_output_dir"): self.output_path_var.set(c.get("General", "custom_output_dir"))
                    if c.has_option("General", "task_mode"): self.task_mode.set(c.get("General", "task_mode"))
                    if c.has_option("General", "enable_grouping"): self.enable_grouping.set(c.getboolean("General", "enable_grouping"))
                    if c.has_option("General", "do_pdf"): self.do_pdf.set(c.getboolean("General", "do_pdf"))
                    if c.has_option("General", "do_word"): self.do_word.set(c.getboolean("General", "do_word"))
                    if c.has_option("General", "do_txt"): self.do_txt.set(c.getboolean("General", "do_txt"))
            except: pass
        if self.startup_path:
            clean = self.startup_path.strip().strip('"').strip("'")
            if os.path.exists(clean): final_path = clean
        if self.startup_out:
            clean_out = self.startup_out.strip().strip('"').strip("'")
            if os.path.exists(clean_out): self.output_path_var.set(clean_out)
        self.path_var.set(final_path)

    def save_settings(self):
        try:
            c = configparser.ConfigParser()
            if os.path.exists(config.CONFIG_FILE): c.read(config.CONFIG_FILE, encoding="utf-8")
            if not c.has_section("General"): c.add_section("General")
            c.set("General", "last_dir", self.path_var.get().strip())
            c.set("General", "custom_output_dir", self.output_path_var.get().strip())
            c.set("General", "task_mode", self.task_mode.get())
            c.set("General", "enable_grouping", str(self.enable_grouping.get()))
            c.set("General", "do_pdf", str(self.do_pdf.get()))
            c.set("General", "do_word", str(self.do_word.get()))
            c.set("General", "do_txt", str(self.do_txt.get()))
            with open(config.CONFIG_FILE, "w", encoding="utf-8") as f: c.write(f)
        except: pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', type=str); parser.add_argument('--out', '-o', type=str)
    args = parser.parse_args()
    start_path = os.path.abspath(args.path) if args.path else None
    start_out = os.path.abspath(args.out) if args.out else None
    root = tk.Tk()
    app = UnifiedApp(root, startup_path=start_path, startup_out=start_out)
    root.mainloop()