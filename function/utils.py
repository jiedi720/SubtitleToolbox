import os
import re
import math

try: import pysrt; HAS_PYSRT = True
except ImportError: HAS_PYSRT = False

# 导入清洗和命名模块
try:
    from function.cleaners import clean_subtitle_text_common, clean_subtitle_text_ass
    from function.naming import clean_filename_title, get_series_name, generate_output_name
except ImportError:
    from function.cleaners import clean_subtitle_text_common, clean_subtitle_text_ass
    from function.naming import clean_filename_title, get_series_name, generate_output_name

# ==========================================================
# 核心工具函数
# ==========================================================

# 1. 基础路径获取 (旧版兼容)
def get_save_path(target_dir, filename):
    script_dir = os.path.join(target_dir, "script")
    if not os.path.exists(script_dir):
        try: os.makedirs(script_dir)
        except: return os.path.join(target_dir, filename)
    return os.path.join(script_dir, filename)

# 2. [新增] 自动分类路径生成器
def get_organized_path(base_output_dir, filename):
    """
    根据文件后缀，自动在 base_output_dir 下创建 txt/word/pdf 子文件夹并返回完整路径。
    """
    ext = os.path.splitext(filename)[1].lower()
    
    # 确定子文件夹名称
    if ext == '.txt': sub = 'txt'
    elif ext == '.docx': sub = 'word'
    elif ext == '.pdf': sub = 'pdf'
    elif ext == '.ass': sub = 'ass_output'
    else: sub = 'other'
    
    # 构造完整目录路径
    final_dir = os.path.join(base_output_dir, sub)
    
    # 自动创建子目录
    if not os.path.exists(final_dir):
        try: os.makedirs(final_dir)
        except: return os.path.join(base_output_dir, filename) # 创建失败则回退到根目录
        
    return os.path.join(final_dir, filename)

# 3. 智能分组
def smart_group_files(file_paths, max_batch_size):
    if not file_paths: return []
    series_dict = {}
    for f in file_paths:
        fname = os.path.basename(f)
        series_key = get_series_name(fname)
        if series_key not in series_dict: series_dict[series_key] = []
        series_dict[series_key].append(f)
    
    final_groups = []
    for key in sorted(series_dict.keys()):
        files = sorted(series_dict[key])
        if max_batch_size <= 0:
            final_groups.append(files)
            continue
        total = len(files)
        num_groups = math.ceil(total / max_batch_size)
        for i in range(num_groups):
            start = i * max_batch_size
            end = start + max_batch_size
            final_groups.append(files[start:end])
    return final_groups

# 4. 递归查找
def find_files_recursively(root_dir, extensions, exclude_dirs=None):
    if exclude_dirs is None: exclude_dirs = ['script', 'Script', 'output', 'Output']
    found_files = []
    for root, dirs, filenames in os.walk(root_dir):
        for d in list(dirs):
            if d in exclude_dirs: dirs.remove(d)
        for filename in filenames:
            if filename.lower().endswith(extensions):
                found_files.append(os.path.join(root, filename))
    return sorted(found_files)

# 5. 万能解析器
def parse_subtitle_to_list(filepath):
    content = ""
    encodings = ['utf-8', 'utf-16', 'utf-8-sig', 'gb18030', 'gbk', 'big5']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f: 
                content = f.read()
                if len(content) > 10: break
        except: continue
    
    if not content: return []

    ext = os.path.splitext(filepath)[1].lower()
    results = []

    if ext == '.srt' and HAS_PYSRT:
        try:
            subs = pysrt.from_string(content)
            for sub in subs:
                t = clean_subtitle_text_common(sub.text)
                if t: results.append((str(sub.start)[:8], t))
            if results: return results
        except: pass

    lines = content.splitlines()
    time_pat = re.compile(r'(\d{1,2}:\d{2}:\d{2})')
    current_time = None
    buffer_text = []

    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith(('WEBVTT', 'Format:', 'Title:', 'Script', '[Script')): continue
        
        if line.startswith('Dialogue:'):
            parts = line.split(',', 9)
            if len(parts) >= 10:
                t_raw = parts[1].strip()
                text_raw = parts[9]
                if t_raw.count(':') == 2:
                    t_clean = t_raw.split('.')[0]
                    if len(t_clean) == 7: t_clean = "0" + t_clean
                else: t_clean = "00:00:00"
                cleaned_text = clean_subtitle_text_common(text_raw)
                if cleaned_text: results.append((t_clean, cleaned_text))
            continue

        if '-->' in line:
            match = time_pat.search(line)
            if match:
                if current_time and buffer_text:
                    full_t = " ".join(buffer_text)
                    cleaned = clean_subtitle_text_common(full_t)
                    if cleaned: results.append((current_time, cleaned))
                t_str = match.group(1)
                if len(t_str) == 7: t_str = "0" + t_str
                current_time = t_str
                buffer_text = []
            continue
        
        if not line.isdigit() and current_time:
            buffer_text.append(line)

    if current_time and buffer_text:
        cleaned = clean_subtitle_text_common(" ".join(buffer_text))
        if cleaned: results.append((current_time, cleaned))

    return results