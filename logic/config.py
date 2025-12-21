#配置文件:存放常量和字体设置。

import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 全局常量
CONFIG_FILE = "SubtitleToolbox.ini"

# 字体配置
FONT_NAME_BODY = 'Batang'
FONT_PATH_BODY = "C:/Windows/Fonts/batang.ttc"
FONT_NAME_ENG = 'Arial'
FONT_PATH_ENG = "C:/Windows/Fonts/arial.ttf"

def init_fonts():
    """初始化 PDF 字体"""
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