"""
配置管理模块
负责处理应用程序的配置文件读写。
"""

import os
import configparser

# 全局常量与路径
# 使用绝对路径，确保在任何工作目录下都能找到配置文件
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SubtitleToolbox.ini")

# 默认 ASS 样式常量
DEFAULT_KOR_STYLE = "Style: KOR - Noto Serif KR,Noto Serif KR SemiBold,20,&H0026FCFF,&H000000FF,&H50000000,&H00000000,-1,0,0,0,100,100,0.1,0,1,0.6,0,2,10,10,34,1"
DEFAULT_CHN_STYLE = "Style: CHN - Drama,小米兰亭,17,&H28FFFFFF,&H000000FF,&H64000000,&H00000000,-1,0,0,0,100,100,0,0,1,0.5,0,2,10,10,15,1"

class SettingsHandler:
    """配置处理类，负责INI配置文件的读写操作"""
    
    @staticmethod
    def load_all_configs():
        """从SubtitleToolbox.ini读取所有配置
        
        Returns:
            dict: 包含所有配置的字典，包括General、Appearance和Presets三个部分
        """
        c = configparser.ConfigParser()
        data = {
            "General": {},
            "Appearance": {"theme": "Light"},
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
        """保存所有配置到SubtitleToolbox.ini
        
        Args:
            settings_dict: 包含设置的字典
            presets_dict: 包含预设的字典
        """
        c = configparser.ConfigParser()
        
        # 写入General部分
        if not c.has_section("General"): 
            c.add_section("General")
        for k, v in settings_dict.items():
            if k != "theme":  # theme单独存放在Appearance
                c.set("General", k, str(v))
        
        # 写入Appearance部分
        if not c.has_section("Appearance"): 
            c.add_section("Appearance")
        c.set("Appearance", "theme", settings_dict.get("theme", "System"))

        # 写入Presets部分
        for name, styles in presets_dict.items():
            if not c.has_section(name): 
                c.add_section(name)
            c.set(name, "kor", styles["kor"])
            c.set(name, "chn", styles["chn"])

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            c.write(f)

    @staticmethod
    def parse_ass_style(style_line):
        """将ASS Style字符串解析为字典
        
        Args:
            style_line: ASS样式字符串
            
        Returns:
            dict: 解析后的样式字典
        """
        parts = style_line.replace("Style:", "").strip().split(',')
        while len(parts) < 23: 
            parts.append("0")
        
        return {
            "font": parts[1].strip(), 
            "size": parts[2].strip(), 
            "color": parts[3].strip(), 
            "bold": 1 if parts[7].strip()=="-1" else 0, 
            "ml": parts[19].strip(), 
            "mr": parts[20].strip(), 
            "mv": parts[21].strip(), 
            "raw": style_line.strip()
        }