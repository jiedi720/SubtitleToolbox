# 工具文件:存放共用的文本处理逻辑。

import os
import re

def clean_subtitle_text_ass(t): 
    """ASS 清洗逻辑"""
    return re.sub(r'\[.*?\]|\(.*?\)|{.*?}', '', t).replace('\n', ' ').replace('\\N', ' ').strip()

def clean_subtitle_text_common(t):
    """PDF/Word 通用清洗逻辑"""
    # 1. 移除标签和换行
    text = re.sub(r'\[.*?\]|\(.*?\)|{.*?}', '', t).replace('\\N', ' ').replace('\n', ' ')
    # 2. 移除不可见 Unicode 控制符
    text = "".join(ch for ch in text if ch.isprintable())
    # 3. 合并空白
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 过滤无效行
    if not text or re.fullmatch(r'[\s\-\.\,\?\!\_]+', text):
        return ""
    return text

def clean_filename_title(n):
    """从文件名提取干净的标题"""
    name = os.path.splitext(n)[0]
    name = re.sub(r'(_track\d+|_?\d+_text).*$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'[. ](19|20)\d{2}([. ]|$)', '.', name)
    stop_keywords = [
        r'Episode', r'2160p', r'1080p', r'720p', r'MULTi', 
        r'NF', r'Netflix', r'WEB-DL', r'WEBrip', r'BluRay', 
        r'DDP5', r'Atmos', r'x265', r'x264', r'CMCTV', r'ARiC'
    ]
    pattern = r'\.(' + '|'.join(stop_keywords) + r')\..*$'
    name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    for kw in [r'Episode', r'MULTi', r'NF', r'CMCTV']:
        name = re.sub(r'\.' + kw + r'.*$', '', name, flags=re.IGNORECASE)
    clean_name = name.replace('.', ' ')
    return re.sub(r'\s+', ' ', clean_name).strip()

def generate_output_name(files, ext=".pdf"):
    """生成输出文件名"""
    first = files[0]
    m = re.search(r'^(.*?)[. ]S\d+E\d+', first, re.IGNORECASE)
    if m:
        series = m.group(1)
        ss = sorted(list(set([int(re.search(r'[. ]S(\d+)E\d+', f, re.IGNORECASE).group(1)) for f in files if re.search(r'[. ]S(\d+)E\d+', f, re.IGNORECASE)])))
        base = f"{series}.S{ss[0]:02d}" if len(ss)==1 else f"{series}.S{ss[0]:02d}-{ss[-1]:02d}"
        return base + ext
    return os.path.splitext(first)[0] + ext