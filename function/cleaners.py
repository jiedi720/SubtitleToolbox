import re

# ==========================================
# 字幕内容清洗模块
# ==========================================

# --- 1. 清洗字幕内容 (通用版) ---
def clean_subtitle_text_common(text):
    if not text: return ""
    
    # 1. 去除 ASS 特效标签 {xxx}
    text = re.sub(r'\{.*?\}', '', text)
    
    # 2. 去除 HTML/SRT 标签 <xxx>
    text = re.sub(r'<.*?>', '', text)
    
    # 3. 去除 方括号 [] 和 圆括号 () 内容 (如音效、旁白)
    text = re.sub(r'\[.*?\]|\(.*?\)', '', text)
    
    # 4. 去除时间轴残留 (00:00:00 --> ...)
    text = re.sub(r'[\d.:,-]+-->[\d.:,-]+', '', text)
    
    # 5. 去除换行符 和 零宽字符/控制字符
    text = text.replace(r'\N', ' ').replace('\n', ' ')
    text = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', text)
    
    # 6. 去除首尾多余符号
    text = re.sub(r'^[-.\s]+', '', text).strip()
    text = re.sub(r'[\s-]+$', '', text).strip()
    
    return text

# --- 2. ASS 专用清洗函数 ---
def clean_subtitle_text_ass(text):
    """
    ASS 专用清洗，仅去除花括号标签
    """
    if not text: return ""
    text = re.sub(r'\{.*?\}', '', text)
    # 如果需要去除音效，可取消注释：
    # text = re.sub(r'\[.*?\]|\(.*?\)', '', text)
    return text.strip()