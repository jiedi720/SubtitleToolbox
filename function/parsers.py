"""
字幕解析与清洗模块
负责将各种格式的字幕文件解析为统一的列表格式，并提供字幕内容清洗功能。
支持SRT、ASS、VTT等格式。
"""

import os
import re

# 尝试导入pysrt库，用于解析SRT格式字幕
try: 
    import pysrt
    HAS_PYSRT = True
except ImportError: 
    HAS_PYSRT = False

__all__ = [
    'parse_subtitle_to_list',
    'clean_subtitle_text_common',
    'clean_subtitle_text_ass'
]


def clean_subtitle_text_common(text):
    """清洗字幕内容 (通用版)：最严格的清洗，适用于提取纯文本
    
    去除特效标签、HTML标签、括号内容、时间轴特征、控制字符等，返回纯净文本。
    
    Args:
        text: 待清洗的字幕文本
        
    Returns:
        str: 清洗后的纯净文本
    """
    if not text: 
        return ""
    
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
    """ASS 专用清洗函数 (增强版)：解决双语合并时的各种问题
    
    专门解决双语合并时出现的音效标注、括号残留及换行符问题，
    支持中、韩、英等多种语言字幕清洗。
    
    Args:
        text: 待清洗的ASS字幕文本
        
    Returns:
        str: 清洗后的ASS字幕文本
    """
    if not text: 
        return ""

    # 1. 去除 ASS/SRT 特效及样式标签 {xxx} 或 <xxx>
    text = re.sub(r'\{.*?\}|<.*?>', '', text)
    
    # 2. 去除方括号 [] 和 圆括号 () 及其内部内容
    # 清除：[의미심장한 음악], (의사1), [영어], （音效）, 【旁白】 等内容
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

def parse_subtitle_to_list(filepath):
    """解析字幕文件为列表格式
    
    支持多种编码尝试，兼容SRT、ASS、VTT等字幕格式，返回清洗后的字幕条目列表。
    
    Args:
        filepath: 字幕文件路径
        
    Returns:
        list: 解析后的字幕列表，每个元素为(时间戳, 清洗后的文本)元组
    """
    content = ""
    # 定义可能用到的编码列表，用于尝试不同编码读取文件
    encodings = ['utf-8', 'utf-16', 'utf-8-sig', 'gb18030', 'gbk', 'big5']
    
    # 遍历所有编码尝试读取文件
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f: 
                content = f.read()
                # 如果读取的内容长度大于10，认为读取成功，跳出循环
                if len(content) > 10: break
        except: 
            continue
    
    if not content: 
        return []
    
    ext = os.path.splitext(filepath)[1].lower()
    results = []

    # 如果文件是SRT格式且pysrt库可用，尝试用pysrt解析
    if ext == '.srt' and HAS_PYSRT:
        try:
            subs = pysrt.from_string(content)
            for sub in subs:
                t = clean_subtitle_text_common(sub.text)
                # 只取时间的前8位（HH:MM:SS格式）
                if t: 
                    results.append((str(sub.start)[:8], t))
            if results: 
                return results
        except: 
            pass

    # 将内容按行分割
    lines = content.splitlines()
    # 编译正则表达式，用于匹配时间戳（HH:MM:SS格式）
    time_pat = re.compile(r'(\d{1,2}:\d{2}:\d{2})')
    current_time = None
    buffer_text = []

    # 遍历每一行
    for line in lines:
        line = line.strip()
        if not line: 
            continue
        # 跳过不需要的元数据行（VTT格式的头部信息等）
        if line.startswith(('WEBVTT', 'Format:', 'Title:', 'Script', '[Script')): 
            continue
        
        # 处理ASS格式字幕行（以'Dialogue:'开头）
        if line.startswith('Dialogue:'):
            parts = line.split(',', 9)
            if len(parts) >= 10:
                t_raw = parts[1].strip()
                text_raw = parts[9]
                # 清理时间戳：如果有两个冒号，取小数点前的部分，否则设为默认值
                t_clean = t_raw.split('.')[0] if t_raw.count(':') == 2 else "00:00:00"
                # 如果时间长度为7（如1:23:45），在前面补0
                if len(t_clean) == 7: 
                    t_clean = "0" + t_clean
                cleaned_text = clean_subtitle_text_common(text_raw)
                if cleaned_text: 
                    results.append((t_clean, cleaned_text))
            continue

        # 处理时间轴行（包含'-->'的行，常见于SRT/VTT格式）
        if '-->' in line:
            match = time_pat.search(line)
            if match:
                # 如果有缓冲文本，先处理缓冲中的文本
                if current_time and buffer_text:
                    cleaned = clean_subtitle_text_common(" ".join(buffer_text))
                    if cleaned: 
                        results.append((current_time, cleaned))
                # 提取匹配到的时间字符串
                t_str = match.group(1)
                # 如果时间长度为7（如1:23:45），在前面补0
                current_time = t_str if len(t_str) == 8 else "0" + t_str
                buffer_text = []
            continue
        
        # 处理字幕文本行（既不是纯数字，又有当前时间戳）
        if not line.isdigit() and current_time:
            buffer_text.append(line)

    # 处理最后一组缓冲的字幕文本（文件末尾的情况）
    if current_time and buffer_text:
        cleaned = clean_subtitle_text_common(" ".join(buffer_text))
        if cleaned: 
            results.append((current_time, cleaned))

    return results