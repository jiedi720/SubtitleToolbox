import os
import re

# ==========================================
# 命名与文件名处理模块
# ==========================================

def clean_filename_title(filename):
    """
    【还原原有逻辑】从文件名中提取纯净的标题。
    保留对单集集数的识别，确保 PDF 内部标题含有 S01E01。
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
    """提取剧集系列名（用于分组）"""
    name = os.path.splitext(filename)[0]
    match = re.search(r'(.*?)[ ._-]*(?:S\d{1,2}|E\d{1,3})', name, re.IGNORECASE)
    if match: 
        return match.group(1).replace('.', ' ').replace('_', ' ').strip().lower()
    return name.split(' ')[0].lower() 

def generate_output_name(filenames, ext=".docx"):
    """
    【核心修复】仅在这里控制总文件名的生成，不影响 PDF 内部标题。
    目标格式: All.of.Us.Are.Dead.S01E01-04.pdf
    """
    if not filenames: return f"merged_output{ext}"
    basenames = [os.path.basename(f) for f in filenames]
    
    # 解析所有文件的集数信息
    pattern_se = re.compile(r'[Ss](\d{1,2})[\s.]*[Ee](\d{1,3})', re.IGNORECASE)
    pattern_e = re.compile(r'[ ._-][Ee](\d{1,3})', re.IGNORECASE)

    parsed_files = []
    for fname in basenames:
        m = pattern_se.search(fname)
        if m:
            parsed_files.append({'s': int(m.group(1)), 'e': int(m.group(2))})
            continue
        m2 = pattern_e.search(fname)
        if m2:
            parsed_files.append({'s': 1, 'e': int(m2.group(1))})
            continue
        parsed_files.append({'s': 999, 'e': 999})

    parsed_files.sort(key=lambda x: (x['s'], x['e']))
    first, last = parsed_files[0], parsed_files[-1]
    
    # --- 修复逻辑开始 ---
    # 1. 拿第一集去洗，得到带 S01E01 的完整标题
    full_title = clean_filename_title(basenames[0])
    
    # 2. 【关键】为了生成总文件名，我们要强行切除标题里的集数部分
    # 这样 All of Us Are Dead S01E01 就会变成 All of Us Are Dead
    series_only = re.sub(r'[._\s]S\d{1,2}[Ee]\d{1,3}.*', '', full_title, flags=re.IGNORECASE).strip()
    
    # 3. 转成点号连接
    final_prefix = series_only.replace(' ', '.')

    if first['s'] == 999:
        return f"{final_prefix}.Batch{len(filenames)}{ext}"

    s_start, e_start = first['s'], first['e']
    s_end, e_end = last['s'], last['e']

    # 4. 拼接总文件名
    if s_start == s_end:
        # Title.S01E01-04.pdf
        return f"{final_prefix}.S{s_start:02d}E{e_start:02d}-{e_end:02d}{ext}"
    else:
        # Title.S01E01-S02E02.pdf
        return f"{final_prefix}.S{s_start:02d}E{e_start:02d}-S{s_end:02d}E{e_end:02d}{ext}"