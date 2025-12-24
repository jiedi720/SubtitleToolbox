#专门负责字幕内容的解析

import os
import re
from function.cleaners import clean_subtitle_text_common

try: 
    import pysrt
    HAS_PYSRT = True
except ImportError: 
    HAS_PYSRT = False

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
                t_clean = t_raw.split('.')[0] if t_raw.count(':') == 2 else "00:00:00"
                if len(t_clean) == 7: t_clean = "0" + t_clean
                cleaned_text = clean_subtitle_text_common(text_raw)
                if cleaned_text: results.append((t_clean, cleaned_text))
            continue

        if '-->' in line:
            match = time_pat.search(line)
            if match:
                if current_time and buffer_text:
                    cleaned = clean_subtitle_text_common(" ".join(buffer_text))
                    if cleaned: results.append((current_time, cleaned))
                t_str = match.group(1)
                current_time = t_str if len(t_str) == 8 else "0" + t_str
                buffer_text = []
            continue
        
        if not line.isdigit() and current_time:
            buffer_text.append(line)

    if current_time and buffer_text:
        cleaned = clean_subtitle_text_common(" ".join(buffer_text))
        if cleaned: results.append((current_time, cleaned))

    return results