import os
import re

# ==========================================
# 命名与文件名处理模块
# ==========================================

def clean_filename_title(filename):
    """
    从文件名中提取纯净的标题（去除 S01E01、年份、分辨率等杂质）
    """
    name = os.path.splitext(filename)[0]
    
    # 提取 S01E01 或 年份之前的标题部分
    match_se = re.search(r'(.*?(?:S\d{1,2}[\s.]?E\d{1,3}|E\d{1,3}))', name, re.IGNORECASE)
    if match_se: 
        name = match_se.group(1)
    else:
        match_year = re.search(r'(.*?)[._\s(\[](19|20)\d{2}', name)
        if match_year: 
            name = match_year.group(1)

    clean_name = name.replace('.', ' ').replace('_', ' ').replace('-', ' ')
    
    # 过滤常见垃圾词
    junk_words = [
        r'\b(19|20)\d{2}\b', r'1080[pi]', r'720[pi]', r'2160[pi]', r'4k', 
        r'WEB.?DL', r'WEB.?Rip', r'BluRay', r'HDTV', r'H\.?264', r'H\.?265', 
        r'x264', r'x265', r'HEVC', r'AAC', r'AC3', r'E.?AC3', r'DDP', r'5\.1', 
        r'Netflix', r'NF', r'AMZN', r'DSNP', r'Subs', r'Repack', r'Proper', 
        r'TC', r'CMCTV', r'text', r'track\d+', r'FRDS'
    ]
    for junk in junk_words: 
        clean_name = re.sub(junk, '', clean_name, flags=re.IGNORECASE)
    
    return re.sub(r'\s+', ' ', clean_name).strip()

def get_series_name(filename):
    """
    提取剧集系列名（用于分组）。
    例如: "Squid.Game.S01E01.srt" -> "squid game"
    """
    name = os.path.splitext(filename)[0]
    match = re.search(r'(.*?)[ ._-]*(?:S\d{1,2}|E\d{1,3})', name, re.IGNORECASE)
    if match: 
        return match.group(1).replace('.', ' ').replace('_', ' ').strip().lower()
    return name.split(' ')[0].lower() # 简单回退策略

def generate_output_name(filenames, ext=".docx"):
    """
    根据一组文件名生成输出文件名。
    例如: [A.S01E01.srt, A.S01E02.srt] -> A.S01E01-E02.docx
    """
    if not filenames: return f"merged_output{ext}"
    
    # 提取纯文件名
    basenames = [os.path.basename(f) for f in filenames]
    
    if len(basenames) == 1: 
        return f"{clean_filename_title(basenames[0]).replace(' ', '.')}{ext}"

    # 正则：匹配 S01E01 或 E01
    pattern_se = re.compile(r'(.*?)[ ._-]*S(\d{1,2})[\s.]*E(\d{1,3})', re.IGNORECASE)
    pattern_e = re.compile(r'(.*?)[ ._-]*E(\d{1,3})', re.IGNORECASE)

    parsed_files = []
    
    for fname in basenames:
        # 尝试匹配 SxxExx
        m = pattern_se.search(fname)
        if m:
            parsed_files.append({'title': m.group(1), 's': int(m.group(2)), 'e': int(m.group(3))})
            continue
        
        # 尝试匹配 Exx (默认为第1季)
        m2 = pattern_e.search(fname)
        if m2:
            parsed_files.append({'title': m2.group(1), 's': 1, 'e': int(m2.group(2))})
            continue
            
        # 匹配失败
        parsed_files.append({'title': fname, 's': 999, 'e': 999})

    # 排序
    parsed_files.sort(key=lambda x: (x['s'], x['e']))
    
    first = parsed_files[0]
    last = parsed_files[-1]
    
    # 如果完全无法解析集数，回退到 Batch 命名
    if first['s'] == 999:
        base = clean_filename_title(basenames[0]).split('.')[0]
        return f"{base}.Batch{len(filenames)}{ext}"

    # 生成标题
    raw_title = clean_filename_title(first['title'])
    final_title = raw_title.replace(' ', '.')

    s_start, e_start = first['s'], first['e']
    s_end, e_end = last['s'], last['e']

    # 格式化输出
    if s_start == s_end:
        # 同一季：Title.S01E01-E04
        return f"{final_title}.S{s_start:02d}E{e_start:02d}-E{e_end:02d}{ext}"
    else:
        # 跨季：Title.S01E01-S02E02
        return f"{final_title}.S{s_start:02d}E{e_start:02d}-S{s_end:02d}E{e_end:02d}{ext}"