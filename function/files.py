"""
文件查找与处理模块
负责文件的递归查找、扫描和分组功能。
"""

import os
from function.naming import get_series_name

__all__ = ['find_files_recursively']

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

