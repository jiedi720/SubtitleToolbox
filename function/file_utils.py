"""
文件工具模块
负责文件查找、路径处理和目录创建等功能。
"""

import os

__all__ = [
    'find_files_recursively',
    'get_organized_path',
    'get_save_path'
]

def find_files_recursively(root_dir, extensions, exclude_dirs=None):
    """递归查找指定后缀的文件，排除特定目录
    
    Args:
        root_dir: 根目录路径
        extensions: 要查找的文件扩展名元组，如 (".txt", ".srt")
        exclude_dirs: 要排除的目录列表，默认为 ['output', 'Output', 'ass', 'Ass']
        
    Returns:
        list: 排序后的文件路径列表
    """
    if exclude_dirs is None: 
        # 不再排除script目录，允许用户直接处理script目录下的文件
        exclude_dirs = ['output', 'Output', 'ass', 'Ass']
    
    found_files = []
    for root, dirs, filenames in os.walk(root_dir):
        # 排除不需要扫描的目录
        for d in list(dirs):
            if d in exclude_dirs: 
                dirs.remove(d)
        
        # 收集符合条件的文件
        for filename in filenames:
            if filename.lower().endswith(extensions):
                found_files.append(os.path.join(root, filename))
    
    return sorted(found_files)


def get_organized_path(base_output_dir, filename):
    """根据文件后缀智能分类文件，生成有组织的路径
    
    分类规则：
    - .ass -> 直接放在 base 目录下
    - .srt -> 放在 base/srt 目录下 (作为原件归档)
    - .txt/.docx/.pdf/.md -> 统一放在 base/script 目录下
    - 其他后缀 -> 放在 base/other 目录中
    
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
    elif ext in ['.txt', '.docx', '.pdf', '.md']:
        # 统一放到 script 目录下
        final_dir = os.path.join(base_output_dir, "script")
    else:
        # 其他类型文件，放到 other 目录中
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