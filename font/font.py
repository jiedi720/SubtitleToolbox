import tkinter as tk
from tkinter import font
import customtkinter as ctk
import re

class FontSelector:
    def __init__(self, master, font_var, root_window):
        """
        仿真 Word 字体选择器组件
        :param master: 放置该组件的父容器 (Frame)
        :param font_var: 绑定的变量 (tk.StringVar)
        :param root_window: 整个应用的根窗口 (用于计算弹窗坐标)
        """
        self.master = master
        self.font_var = font_var
        self.root = root_window
        self.active_dropdown = None
        
        # 1. 预载并过滤系统字体 (@开头为竖排字体，予以屏蔽)
        try:
            raw_fonts = list(font.families())
            self.all_fonts = sorted([
                f for f in set(raw_fonts) 
                if f and not f.startswith("@")
            ])
            if not self.all_fonts:
                self.all_fonts = ["Arial", "Courier New", "Microsoft YaHei", "SimSun"]
        except:
            self.all_fonts = ["Arial", "Courier New", "Microsoft YaHei"]
            
        self.setup_ui()

    def setup_ui(self):
        # 组件容器
        self.container = ctk.CTkFrame(self.master, fg_color="transparent")
        self.container.pack(fill="x", side="left", expand=True)

        # 【核心修复】生命周期绑定：当父容器销毁（如配置窗口关闭）时，强制关闭下拉列表
        self.container.bind("<Destroy>", lambda e: self.close_dropdown())

        # 1. 字体输入框 (支持手动输入和实时搜索)
        self.font_entry = ctk.CTkEntry(
            self.container, 
            textvariable=self.font_var, 
            height=28
        )
        self.font_entry.pack(side="left", fill="x", expand=True)
        self.font_entry.bind("<KeyRelease>", self.on_key_release)

        # 2. 下拉箭头按钮
        self.arrow_btn = ctk.CTkButton(
            self.container, 
            text="▼", 
            width=30, 
            height=28, 
            fg_color="#3b8ed0", 
            command=lambda: self.toggle_dropdown(force_all=True)
        )
        self.arrow_btn.pack(side="left", padx=(2, 0))

    def on_key_release(self, event):
        """处理键盘输入：过滤功能键并触发搜索列表"""
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            if event.keysym == "Escape": self.close_dropdown()
            return
        # 只要开始打字，就弹出过滤后的列表
        self.toggle_dropdown(force_all=False)

    def toggle_dropdown(self, force_all=False):
        """切换下拉列表显示"""
        # 如果点击按钮时列表已开，则关闭
        if self.active_dropdown and self.active_dropdown.winfo_exists():
            self.close_dropdown()
            if force_all: return

        # 创建无边框弹出层
        self.active_dropdown = ctk.CTkToplevel(self.root)
        self.active_dropdown.overrideredirect(True) # 隐藏边框和任务栏
        self.active_dropdown.attributes("-topmost", True)
        
        # 确保窗口能捕获焦点以触发 FocusOut
        self.active_dropdown.after(10, self.active_dropdown.focus_set)
        
        # 刷新坐标计算
        self.root.update_idletasks()
        try:
            x = self.font_entry.winfo_rootx()
            y = self.font_entry.winfo_rooty() + self.font_entry.winfo_height()
            w = self.container.winfo_width()
            self.active_dropdown.geometry(f"{w}x250+{x}+{y}")
        except:
            return

        # 滚动容器：提供宽大易拖拽的滚动条
        self.scroll = ctk.CTkScrollableFrame(
            self.active_dropdown, 
            corner_radius=0, 
            fg_color=("#f2f2f2", "#2b2b2b"),
            scrollbar_button_color="#3b8ed0",
            scrollbar_button_hover_color="#1f538d"
        )
        self.scroll.pack(fill="both", expand=True)

        # 过滤逻辑
        typed = self.font_var.get().strip().lower()
        if force_all or not typed:
            display_list = self.all_fonts
        else:
            display_list = [f for f in self.all_fonts if typed in f.lower()]
            # 如果没搜到匹配项，回退显示全量列表
            if not display_list: display_list = self.all_fonts

        # 性能保护：限制首屏加载数量
        self._load_font_buttons(display_list[:100])

        # --- 绑定关闭事件组 ---
        # 1. 点击窗口外部关闭
        self.root.bind_all("<Button-1>", self.check_click_outside, add="+")
        # 2. 窗口失去焦点关闭
        self.active_dropdown.bind("<FocusOut>", lambda e: self.close_dropdown())
        # 3. 按 ESC 键关闭
        self.active_dropdown.bind("<Escape>", lambda e: self.close_dropdown())

    def check_click_outside(self, event):
        """全局点击检查：点击非组件区域时关闭下拉框"""
        if not self.active_dropdown or not self.active_dropdown.winfo_exists():
            return
        
        # 获取点击的屏幕坐标
        x, y = event.x_root, event.y_root
        
        # 获取下拉框的屏幕范围
        dx = self.active_dropdown.winfo_rootx()
        dy = self.active_dropdown.winfo_rooty()
        dw = self.active_dropdown.winfo_width()
        dh = self.active_dropdown.winfo_height()

        # 判定逻辑：如果点击不在下拉框内，且不是点在输入框或箭头按钮上
        if not (dx <= x <= dx + dw and dy <= y <= dy + dh):
            if event.widget not in (self.font_entry, self.arrow_btn):
                self.close_dropdown()

    def _load_font_buttons(self, fonts):
        """分片渲染字体按钮以防界面卡顿"""
        for f in fonts:
            btn = ctk.CTkButton(
                self.scroll, 
                text=f, 
                font=(f, 11), 
                fg_color="transparent", 
                text_color=("black", "white"), 
                anchor="w", 
                height=28, 
                hover_color=("#d0d0d0", "#3d3d3d"),
                command=lambda name=f: self.set_font(name)
            )
            btn.pack(fill="x")

    def set_font(self, name):
        """选定字体并关闭"""
        self.font_var.set(name)
        self.close_dropdown()

    def close_dropdown(self):
        """显式销毁下拉窗口并解除全局绑定"""
        if self.active_dropdown:
            try:
                # 必须解除全局绑定，否则主窗口操作会受干扰
                self.root.unbind_all("<Button-1>")
            except:
                pass
            
            if self.active_dropdown.winfo_exists():
                try:
                    self.active_dropdown.destroy()
                except:
                    pass
            self.active_dropdown = None