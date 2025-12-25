#专门负责路径生成、分类和目录创建逻辑。

import os

def get_organized_path(base_output_dir, filename):
    """
    根据后缀智能分类：
    - .ass -> 直接放在 base 目录下 (不再进入 ass 子文件夹)
    - .srt -> 放在 base/srt 目录下 (作为原件归档)
    - .txt/.docx/.pdf -> 保持原有分类逻辑
    """
    ext = os.path.splitext(filename)[1].lower()
    
    # 1. 路径纠偏：如果用户选的是 script 或 srt 目录，退回一级到根目录
    if os.path.basename(base_output_dir).lower() in ['script', 'srt']:
        base_output_dir = os.path.dirname(base_output_dir)

    # 2. 逻辑分流
    if ext == '.ass':
        # --- 核心改动：ASS 文件直接放在源目录 ---
        final_dir = base_output_dir 
    elif ext == '.srt':
        # --- 核心改动：SRT 文件进入专门的归档目录 ---
        final_dir = os.path.join(base_output_dir, "srt")
    elif ext in ['.txt', '.docx', '.pdf']:
        sub_folder = 'txt' if ext == '.txt' else ('word' if ext == '.docx' else 'pdf')
        final_dir = os.path.join(base_output_dir, "script", sub_folder)
    else:
        final_dir = os.path.join(base_output_dir, "script", "other")

    # 3. 按需创建文件夹
    if final_dir != base_output_dir and not os.path.exists(final_dir):
        try:
            os.makedirs(final_dir, exist_ok=True)
        except:
            return os.path.join(base_output_dir, filename)
            
    return os.path.join(final_dir, filename)

def get_save_path(target_dir, filename):
    """旧版接口兼容"""
    return get_organized_path(target_dir, filename)