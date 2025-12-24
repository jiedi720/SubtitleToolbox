import re

# ==========================================
# 字幕内容清洗模块 (v3.1)
# ==========================================

def clean_subtitle_text_common(text):
    """
    清洗字幕内容 (通用版)：最严格的清洗，适用于提取纯文本
    """
    if not text: return ""
    
    # 1. 去除 ASS 特效标签 {xxx}
    text = re.sub(r'\{.*?\}', '', text)
    
    # 2. 去除 HTML/SRT 标签 <xxx>
    text = re.sub(r'<.*?>', '', text)
    
    # 3. 去除 方括号 [] 和 圆括号 () 内容 (通常为音效描述、旁白)
    text = re.sub(r'\[.*?\]|\(.*?\)', '', text)
    
    # 4. 去除可能残留的时间轴特征 (如 00:00:00 --> ...)
    text = re.sub(r'[\d.:,-]+-->[\d.:,-]+', '', text)
    
    # 5. 去除零宽字符、控制字符 (防止某些编辑器显示乱码)
    text = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', text)
    
    # 6. 处理换行：将 \N 和 物理换行符 统一替换为空格
    text = text.replace(r'\N', ' ').replace('\n', ' ').replace('\r', ' ')
    
    # 7. 去除首尾多余符号 (如横杠、点、空格)
    text = re.sub(r'^[-.\s]+', '', text).strip()
    text = re.sub(r'[\s-]+$', '', text).strip()
    
    # 8. 合并连续的多个空格为单个空格
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def clean_subtitle_text_ass(text):
    """
    ASS 专用清洗函数 (增强版)：
    专门解决双语合并时出现的音效标注、括号残留及换行符问题。
    """
    if not text: return ""

    # 1. 去除 ASS/SRT 特效及样式标签 {xxx} 或 <xxx>
    text = re.sub(r'\{.*?\}|<.*?>', '', text)
    
    # 2. 【新增】去除方括号 [] 和 圆括号 () 及其内部内容
    # 这将清除：[의미심장한 음악], (의사1), [영어] 等内容
    text = re.sub(r'\[.*?\]|\(.*?\)|（.*?）|【.*?】', '', text)
    
    # 3. 将硬换行 \N 或 \n 替换为空格
    text = text.replace(r'\N', ' ').replace('\n', ' ').replace('\r', ' ')
    
    # 4. 去除零宽字符、控制字符
    text = re.sub(r'[\u200b-\u200f\ufeff]', '', text)
    
    # 5. 去除首尾多余的符号（如横杠、点、多余空格）
    # 很多韩语字幕开头会有 "- " 表示对话开始，制作 ASS 时通常不需要
    text = re.sub(r'^[-.\s]+', '', text).strip()
    
    # 6. 合并重复空格并修剪
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text