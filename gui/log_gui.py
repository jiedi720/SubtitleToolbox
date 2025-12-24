import tkinter as tk
import customtkinter as ctk

class LogComponent:
    def __init__(self, parent):
        self.parent = parent
        
        # 颜色常量定义
        self.colors = {
            "dark_bg": "#1d1e1e",
            "light_bg": "#f9f9f9",
            "dark_fg": "#ffffff",
            "light_fg": "#000000",
            "pdf_red": "#FC0273",
            "word_blue": "#2189CF",
            "success_green": "#2ecc71", # 路径成功绿色
            "error_red": "#e74c3c"      # 路径失败红色
        }
        
        self.setup_ui()

    def setup_ui(self):
        # 初始检测主题
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg = self.colors["dark_bg"] if is_dark else self.colors["light_bg"]
        fg = self.colors["dark_fg"] if is_dark else self.colors["light_fg"]

        # 创建原生 Text 组件以确保颜色标签 100% 生效
        self.widget = tk.Text(
            self.parent, 
            height=8,
            font=("Microsoft YaHei", 10),
            bg=bg,
            fg=fg,
            padx=12,
            pady=12,
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#3d3d3d" if is_dark else "#dbdbdb",
            insertbackground=fg
        )
        
        # 注册持久化的颜色标签
        self.widget.tag_config("pdf_red", foreground=self.colors["pdf_red"])
        self.widget.tag_config("word_blue", foreground=self.colors["word_blue"])
        # --- 新增颜色标签 ---
        self.widget.tag_config("success", foreground=self.colors["success_green"])
        self.widget.tag_config("error", foreground=self.colors["error_red"])
        
        self.widget.configure(state='disabled')

    def update_theme(self, mode):
        """当系统切换主题时，手动调整原生组件颜色"""
        is_dark = (mode == "Dark")
        bg = self.colors["dark_bg"] if is_dark else self.colors["light_bg"]
        fg = self.colors["dark_fg"] if is_dark else self.colors["light_fg"]
        border = "#3d3d3d" if is_dark else "#dbdbdb"
        
        self.widget.configure(
            bg=bg, 
            fg=fg, 
            highlightbackground=border, 
            insertbackground=fg
        )

    def clear(self):
        """清空日志区域"""
        self.widget.configure(state='normal')
        self.widget.delete("1.0", tk.END)
        self.widget.configure(state='disabled')

    def write_log(self, message, tag=None):
        """写入日志内容"""
        self.widget.configure(state='normal')
        
        # 如果传入的是 success 或 error，会自动应用上面 tag_config 定义的颜色
        if tag:
            self.widget.insert(tk.END, str(message) + "\n", tag)
        else:
            self.widget.insert(tk.END, str(message) + "\n")
            
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')

    def append(self, message):
        """为了兼容性增加的别名方法"""
        self.write_log(message)