import os
import tkinter as tk
import customtkinter as ctk
from config.settings import CONFIG_FILE, SettingsHandler, init_fonts
from font.ass import DEFAULT_KOR_STYLE, DEFAULT_CHN_STYLE

class BaseController:
    def __init__(self, root, startup_path=None, startup_out=None):
        self.root = root
        self.config_file = CONFIG_FILE
        
        try: init_fonts()
        except: pass

        self.default_kor_raw = DEFAULT_KOR_STYLE
        self.default_chn_raw = DEFAULT_CHN_STYLE

        self._init_vars()
        self.load_settings()
        ctk.set_appearance_mode(self.theme_mode)

        # 加载预设
        raw_config = SettingsHandler.load_all_configs()
        self.presets = raw_config.get("Presets", {})
        if not self.presets:
            self.presets = {"默认": {"kor": self.default_kor_raw, "chn": self.default_chn_raw}}
        
        current_name = self.current_preset_name.get()
        if current_name not in self.presets:
            current_name = list(self.presets.keys())[0]
            self.current_preset_name.set(current_name)
        
        self.refresh_parsed_styles()

    def _init_vars(self):
        self.path_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.current_preset_name = tk.StringVar(value="默认")
        self.task_mode = tk.StringVar(value="ASS")
        self.do_pdf = tk.BooleanVar(value=True)
        self.do_word = tk.BooleanVar(value=True)
        self.do_txt = tk.BooleanVar(value=True)
        self.enable_grouping = tk.BooleanVar(value=False)
        self.theme_mode = "System"

    def refresh_parsed_styles(self):
        curr_preset = self.presets[self.current_preset_name.get()]
        self.kor_parsed = SettingsHandler.parse_ass_style(curr_preset["kor"])
        self.chn_parsed = SettingsHandler.parse_ass_style(curr_preset["chn"])

    def load_settings(self):
        data = SettingsHandler.load_all_configs()
        gen = data.get("General", {})
        self.path_var.set(gen.get("last_dir", "C:/"))
        self.output_path_var.set(gen.get("custom_output_dir", ""))
        self.task_mode.set(gen.get("task_mode", "ASS"))
        self.enable_grouping.set(gen.get("enable_grouping", "False") == "True")
        self.do_pdf.set(gen.get("do_pdf", "True") == "True")
        self.do_word.set(gen.get("do_word", "True") == "True")
        self.do_txt.set(gen.get("do_txt", "True") == "True")
        self.theme_mode = data.get("Appearance", {}).get("theme", "System")

    def save_settings(self):
        current_gen = {
            "last_dir": self.path_var.get().strip(),
            "custom_output_dir": self.output_path_var.get().strip(),
            "task_mode": self.task_mode.get(),
            "enable_grouping": str(self.enable_grouping.get()),
            "do_pdf": str(self.do_pdf.get()),
            "do_word": str(self.do_word.get()),
            "do_txt": str(self.do_txt.get()),
            "theme": self.theme_mode
        }
        SettingsHandler.save_all_configs(current_gen, self.presets)

    def log(self, message, tag=None):
        if hasattr(self.gui, 'log_area'):
            self.gui.log_area.write_log(message, tag)