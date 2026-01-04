"""
路径处理模块
负责路径生成、分类和目录创建逻辑，根据文件后缀智能分类文件。
"""

import os

__all__ = [
    'get_organized_path',
    'get_save_path'
]

def get_organized_path(base_output_dir, filename):
    """根据文件后缀智能分类文件，生成有组织的路径
    
    分类规则：
    - .ass -> 直接放在 base 目录下
    - .srt -> 放在 base/srt 目录下 (作为原件归档)
    - .txt/.docx/.pdf -> 分别放在对应的子目录中
    - 其他后缀 -> 放在 other 目录中
    
    Args:
        base_output_dir: 基础输出目录
        filename: 文件名
        
    Returns:
        str: 生成的完整文件路径
    """
    ext = os.path.splitext(filename)[1].lower()
    
    # 逻辑分流：根据文件后缀确定最终目录
    if ext == '.ass':
        # ASS 文件直接放在源目录
        final_dir = base_output_dir 
    elif ext == '.srt':
        # SRT 文件进入专门的归档目录
        final_dir = os.path.join(base_output_dir, "srt")
    elif ext in ['.txt', '.docx', '.pdf']:
        # 根据文件类型确定子文件夹，直接放在目标目录下，不再生成script文件夹
        sub_folder = 'txt' if ext == '.txt' else ('word' if ext == '.docx' else 'pdf')
        final_dir = os.path.join(base_output_dir, sub_folder)
    else:
        # 其他类型文件，直接放在目标目录下，不再生成script文件夹
        final_dir = os.path.join(base_output_dir, "other")

    # 按需创建文件夹
    if final_dir != base_output_dir and not os.path.exists(final_dir):
        try:
            os.makedirs(final_dir, exist_ok=True)
        except:
            # 创建文件夹失败时，返回基础目录下的路径
            return os.path.join(base_output_dir, filename)
            
    return os.path.join(final_dir, filename)

def get_save_path(target_dir, filename):
    """旧版接口兼容，调用get_organized_path函数
    
    Args:
        target_dir: 目标目录
        filename: 文件名
        
    Returns:
        str: 生成的完整文件路径
    """
    return get_organized_path(target_dir, filename)