#专门负责路径生成、分类和目录创建逻辑。

import os

def get_organized_path(base_output_dir, filename):
    """
    根据后缀智能分类：
    - .txt/.docx/.pdf -> base/script/[txt|word|pdf]
    - .ass -> base/ass
    """
    ext = os.path.splitext(filename)[1].lower()
    
    # 路径纠偏：如果传入的是已存在的 script 目录，退回一级
    if os.path.basename(base_output_dir).lower() == 'script':
        base_output_dir = os.path.dirname(base_output_dir)

    # 逻辑分流
    if ext == '.ass':
        # 纯 ASS 逻辑：完全不涉及 script 字符串
        final_dir = os.path.join(base_output_dir, "ass")
    elif ext in ['.txt', '.docx', '.pdf']:
        # 文档逻辑：包含 script 文件夹
        sub_folder = 'txt' if ext == '.txt' else ('word' if ext == '.docx' else 'pdf')
        final_dir = os.path.join(base_output_dir, "script", sub_folder)
    else:
        # 其他兜底
        final_dir = os.path.join(base_output_dir, "script", "other")

    # 按需创建：只有确定需要这个路径时才创建文件夹
    if not os.path.exists(final_dir):
        try:
            os.makedirs(final_dir, exist_ok=True)
        except:
            return os.path.join(base_output_dir, filename)
            
    return os.path.join(final_dir, filename)

def get_save_path(target_dir, filename):
    """旧版接口兼容"""
    return get_organized_path(target_dir, filename)