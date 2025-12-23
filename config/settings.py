import os
import configparser
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ==========================================
# 1. 全局常量与路径
# ==========================================
CONFIG_FILE = "SubtitleToolbox.ini"

# 字体配置路径
FONT_NAME_BODY = 'Batang'
FONT_PATH_BODY = "C:/Windows/Fonts/batang.ttc"
FONT_NAME_ENG = 'Arial'
FONT_PATH_ENG = "C:/Windows/Fonts/arial.ttf"

def init_fonts():
    """初始化 PDF 报表所需的字体"""
    global FONT_NAME_BODY, FONT_NAME_ENG
    try:
        if os.path.exists(FONT_PATH_BODY):
            pdfmetrics.registerFont(TTFont(FONT_NAME_BODY, FONT_PATH_BODY, subfontIndex=0))
        else:
            fallback = "C:/Windows/Fonts/malgun.ttf"
            if os.path.exists(fallback):
                FONT_NAME_BODY = 'MalgunGothic'
                pdfmetrics.registerFont(TTFont(FONT_NAME_BODY, fallback))
            else:
                FONT_NAME_BODY = 'Helvetica'
        
        if os.path.exists(FONT_PATH_ENG):
            pdfmetrics.registerFont(TTFont(FONT_NAME_ENG, FONT_PATH_ENG))
        else:
            FONT_NAME_ENG = 'Helvetica'
    except Exception:
        FONT_NAME_BODY = 'Helvetica'
        FONT_NAME_ENG = 'Helvetica'
    
    return FONT_NAME_BODY, FONT_NAME_ENG

# ==========================================
# 2. 配置处理类 (INI 读写)
# ==========================================
class SettingsHandler:
    @staticmethod
    def load_all_configs():
        """从 SubtitleToolbox.ini 读取所有配置"""
        c = configparser.ConfigParser()
        data = {
            "General": {},
            "Appearance": {"theme": "System"},
            "Presets": {}
        }
        if os.path.exists(CONFIG_FILE):
            try:
                c.read(CONFIG_FILE, encoding="utf-8")
                # 读取通用设置
                if c.has_section("General"):
                    data["General"] = dict(c.items("General"))
                # 读取主题设置
                if c.has_section("Appearance"):
                    data["Appearance"]["theme"] = c.get("Appearance", "theme", fallback="System")
                # 读取预设 (排除 General 和 Appearance)
                for section in c.sections():
                    if section not in ["General", "Appearance"]:
                        data["Presets"][section] = {
                            "kor": c.get(section, "kor"),
                            "chn": c.get(section, "chn")
                        }
            except Exception as e:
                print(f"配置文件读取失败: {e}")
        return data

    @staticmethod
    def save_all_configs(settings_dict, presets_dict):
        """保存所有配置到 SubtitleToolbox.ini"""
        c = configparser.ConfigParser()
        
        # 写入 General
        if not c.has_section("General"): c.add_section("General")
        for k, v in settings_dict.items():
            if k != "theme": # theme 单独存放在 Appearance
                c.set("General", k, str(v))
        
        # 写入 Appearance
        if not c.has_section("Appearance"): c.add_section("Appearance")
        c.set("Appearance", "theme", settings_dict.get("theme", "System"))

        # 写入 Presets
        for name, styles in presets_dict.items():
            if not c.has_section(name): c.add_section(name)
            c.set(name, "kor", styles["kor"])
            c.set(name, "chn", styles["chn"])

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            c.write(f)

    @staticmethod
    def parse_ass_style(style_line):
        """将 ASS Style 字符串解析为字典"""
        parts = style_line.replace("Style:", "").strip().split(',')
        while len(parts) < 23: parts.append("0")
        return {
            "font": parts[1].strip(), "size": parts[2].strip(), 
            "color": parts[3].strip(), "bold": 1 if parts[7].strip()=="-1" else 0, 
            "ml": parts[19].strip(), "mr": parts[20].strip(), 
            "mv": parts[21].strip(), "raw": style_line.strip()
        }