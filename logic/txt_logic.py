import os
import re
import sys
from tkinter import messagebox

# 尝试导入 pysrt
try:
    import pysrt
    HAS_PYSRT = True
except ImportError:
    HAS_PYSRT = False

# 尝试从 utils 导入
try:
    from utils import clean_subtitle_text_common, clean_filename_title, generate_output_name
except ImportError:
    # 后备逻辑
    def clean_subtitle_text_common(t):
        t = re.sub(r'\[.*?\]|\(.*?\)|{.*?}', '', t).replace('\n', ' ')
        return t.strip()
    def clean_filename_title(n): return os.path.splitext(n)[0]
    def generate_output_name(files, ext=".txt"): return f"merged_output{ext}"

def read_file_content(filepath):
    """
    智能编码读取
    """
    encodings = ['utf-8', 'utf-8-sig', 'gb18030', 'gbk', 'big5', 'utf-16', 'euc-kr', 'shift_jis']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

def extract_content_with_timestamps(filepath):
    """
    提取带时间轴的内容 [00:00:06] 内容
    """
    raw_content = read_file_content(filepath)
    if not raw_content:
        return "[读取失败]"

    ext = os.path.splitext(filepath)[1].lower()
    output_lines = []

    # === 策略 A: pysrt (推荐) ===
    if ext == '.srt' and HAS_PYSRT:
        try:
            subs = pysrt.from_string(raw_content)
            for sub in subs:
                txt = clean_subtitle_text_common(sub.text)
                if txt:
                    time_str = str(sub.start)[:8]
                    output_lines.append(f"[{time_str}]  {txt}")
            return "\n".join(output_lines)
        except Exception:
            pass

    # === 策略 B: 正则提取 (适用于 VTT 或 解析失败的 SRT) ===
    timestamp_pattern = re.compile(r'^\s*(\d{1,2}:\d{2}:\d{2})[,.]\d{3}\s*-->')
    
    lines = raw_content.splitlines()
    current_time = None
    current_text_buffer = []

    for line in lines:
        line = line.strip()
        if not line:
            if current_time and current_text_buffer:
                full_text = " ".join(current_text_buffer)
                cleaned_text = clean_subtitle_text_common(full_text)
                if cleaned_text:
                    output_lines.append(f"[{current_time}]  {cleaned_text}")
            current_time = None
            current_text_buffer = []
            continue
        
        ts_match = timestamp_pattern.match(line)
        if ts_match:
            t_str = ts_match.group(1)
            if len(t_str) == 7: t_str = "0" + t_str
            current_time = t_str
            continue
            
        if line.isdigit(): continue
        if line.startswith('WEBVTT') or line.startswith('[Script Info]') or line.startswith('Format:'): continue

        if current_time is not None:
            current_text_buffer.append(line)

    if current_time and current_text_buffer:
        full_text = " ".join(current_text_buffer)
        cleaned_text = clean_subtitle_text_common(full_text)
        if cleaned_text:
            output_lines.append(f"[{current_time}]  {cleaned_text}")

    # 如果没有提取到时间轴，返回纯文本
    if not output_lines:
        return raw_content

    return "\n".join(output_lines)

def run_txt_creation_task(target_dir, log_func, progress_bar, root):
    """
    任务1: 字幕转 TXT (SRT/VTT -> 汇总 TXT)
    读取所有字幕文件，提取时间轴和内容，生成一个汇总剧本文件。
    """
    log_func(f"[SRT->TXT] 正在扫描字幕文件: {target_dir}")

    # 只扫描字幕格式
    subtitle_extensions = ('.srt', '.vtt', '.ass', '.smi')
    files = []
    
    try:
        all_items = os.listdir(target_dir)
        for item in all_items:
            if item.lower().endswith(subtitle_extensions):
                full_path = os.path.join(target_dir, item)
                if os.path.isfile(full_path):
                    files.append(full_path)
    except Exception as e:
        log_func(f"❌ 扫描出错: {e}")
        return

    files.sort()

    if not files:
        log_func(f"[SRT->TXT] 未找到字幕文件 (.srt, .vtt等)。")
        return

    total_files = len(files)
    log_func(f"[SRT->TXT] 找到 {total_files} 个字幕文件，准备生成剧本...")
    
    progress_bar["maximum"] = total_files
    progress_bar["value"] = 0

    # 生成文件名
    filenames_only = [os.path.basename(f) for f in files]
    output_filename = generate_output_name(filenames_only, ext=".txt")
    output_path = os.path.join(target_dir, output_filename)
    
    if output_path in files: files.remove(output_path)

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for index, file_path in enumerate(files):
                file_name = os.path.basename(file_path)
                nice_title = clean_filename_title(file_name)
                
                log_func(f"正在处理 [{index+1}/{total_files}]: {nice_title}")
                
                # 调用带时间轴的提取
                content = extract_content_with_timestamps(file_path)
                
                outfile.write("="*60 + "\n")
                outfile.write(f"【{nice_title}】\n")
                outfile.write("="*60 + "\n\n")
                
                outfile.write(content)
                outfile.write("\n\n\n")

                progress_bar["value"] = index + 1
                root.update_idletasks()
        
        log_func("-" * 30)
        log_func(f"[SRT->TXT] ✅ 剧本生成成功! 文件: {output_filename}")

    except Exception as e:
        log_func(f"❌ 错误: {str(e)}")
        messagebox.showerror("错误", str(e))
    finally:
        progress_bar["value"] = 0

def run_txt_merge_task(target_dir, log_func, progress_bar, root):
    """
    任务2: TXT 合并 (TXT -> 汇总 TXT)
    简单合并目录下现有的 .txt 文件。
    """
    log_func(f"[TXT合并] 正在扫描 TXT 文件: {target_dir}")

    files = []
    try:
        all_items = os.listdir(target_dir)
        for item in all_items:
            # 只扫描 .txt
            if item.lower().endswith('.txt'):
                # 排除可能已经存在的“合并后”的文件，防止循环包含
                if "合并后的文本" in item or "merged_output" in item or "全剧本" in item:
                    continue
                
                full_path = os.path.join(target_dir, item)
                if os.path.isfile(full_path):
                    files.append(full_path)
    except Exception as e:
        log_func(f"❌ 扫描出错: {e}")
        return

    files.sort()

    if not files:
        log_func(f"[TXT合并] 未找到 .txt 文件。")
        return

    total_files = len(files)
    log_func(f"[TXT合并] 找到 {total_files} 个 TXT 文件，准备合并...")
    
    progress_bar["maximum"] = total_files
    progress_bar["value"] = 0

    # 生成输出文件名
    dir_name = os.path.basename(target_dir)
    output_filename = f"全剧本.txt"
    output_path = os.path.join(target_dir, output_filename)
    
    if output_path in files: files.remove(output_path)

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for index, file_path in enumerate(files):
                file_name = os.path.basename(file_path)
                
                log_func(f"正在合并 [{index+1}/{total_files}]: {file_name}")
                
                # 简单读取内容
                content = read_file_content(file_path)
                
                outfile.write("="*60 + "\n")
                outfile.write(f"文件名: {file_name}\n")
                outfile.write("="*60 + "\n\n")
                
                outfile.write(content)
                outfile.write("\n\n\n")

                progress_bar["value"] = index + 1
                root.update_idletasks()
        
        log_func("-" * 30)
        log_func(f"[TXT合并] ✅ 成功! 输出文件:  {output_filename}")

    except Exception as e:
        log_func(f"❌ 错误: {str(e)}")
        messagebox.showerror("错误", str(e))
    finally:
        progress_bar["value"] = 0