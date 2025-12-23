import customtkinter as ctk

def create_path_row(parent, label_text, variable, btns_cfg, ui_font, ui_font_small, text_color):
    """
    通用路径行组件：包含标签、输入框和一组功能按钮
    """
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=5, padx=10)
    
    ctk.CTkLabel(row, text=label_text, font=ui_font_small, width=90, anchor="e").pack(side="left")
    
    entry = ctk.CTkEntry(row, textvariable=variable, font=ui_font, height=34, text_color=text_color)
    entry.pack(side="left", fill="x", expand=True, padx=10)

    # 按钮样式配置
    btn_style = {
        "fg_color": "transparent", "border_width": 1,
        "border_color": ("#000000", "#FFFFFF"),
        "width": 30, "height": 30,
        "text_color": ("#000000", "#FFFFFF"),
        "font": ("Segoe UI Emoji", 17),
        "hover": False
    }

    def _on_hover(e, b, mode="enter"):
        theme = ctk.get_appearance_mode()
        if mode == "enter":
            bg = "#000000" if theme == "Light" else "#FFFFFF"
            fg = "#FFFFFF" if theme == "Light" else "#000000"
            b.configure(fg_color=bg, text_color=fg)
        else:
            b.configure(fg_color="transparent", text_color=("#000000", "#FFFFFF"))

    for icon, cmd in btns_cfg:
        btn = ctk.CTkButton(row, text=icon, command=cmd, **btn_style)
        btn.pack(side="left", padx=2)
        btn.bind("<Enter>", lambda e, b=btn: _on_hover(e, b, "enter"))
        btn.bind("<Leave>", lambda e, b=btn: _on_hover(e, b, "leave"))
        btn.bind("<Button-1>", lambda e, b=btn: b.configure(fg_color="#3b8ed0", text_color="#FFFFFF"))
        btn.bind("<ButtonRelease-1>", lambda e, b=btn: _on_hover(e, b, "enter"))
    
    return entry