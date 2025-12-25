# 专门负责文件查找、扫描和分组

import os
import math
from function.naming import get_series_name

def find_files_recursively(root_dir, extensions, exclude_dirs=None):
    """
    递归查找指定后缀的文件，排除特定目录
    """
    if exclude_dirs is None: 
        exclude_dirs = ['script', 'Script', 'output', 'Output', 'ass', 'Ass']
    found_files = []
    for root, dirs, filenames in os.walk(root_dir):
        # 排除不需要扫描的目录
        for d in list(dirs):
            if d in exclude_dirs: 
                dirs.remove(d)
        for filename in filenames:
            if filename.lower().endswith(extensions):
                found_files.append(os.path.join(root, filename))
    return sorted(found_files)

def smart_group_files(file_paths, max_batch_size):
    """
    智能分组逻辑：保证每个分卷的集数尽可能平均。
    例如：10集限制最大4集时，会分成 4+3+3；6集限制4集时，会分成 3+3。
    """
    if not file_paths: return []
    
    # 按剧集名称进行归类
    series_dict = {}
    for f in file_paths:
        fname = os.path.basename(f)
        series_key = get_series_name(fname)
        if series_key not in series_dict: 
            series_dict[series_key] = []
        series_dict[series_key].append(f)
    
    final_groups = []
    # 按照剧集名称排序处理
    for key in sorted(series_dict.keys()):
        files = sorted(series_dict[key])
        total = len(files)
        
        # 如果不限制每包大小，则全部放入一组
        if max_batch_size <= 0:
            final_groups.append(files)
            continue
        
        # --- 核心平摊算法 ---
        # 1. 计算总共需要分成几个组
        num_groups = math.ceil(total / max_batch_size)
        
        # 2. 计算每组的基础大小 (base_size) 和 多出来的余数 (remainder)
        # 例如 10 // 3 = 3 (每组基础3集), 10 % 3 = 1 (多出1集)
        base_size = total // num_groups
        remainder = total % num_groups
        
        # 3. 分配文件到各组
        start = 0
        for i in range(num_groups):
            # 如果当前组的索引小于余数，则该组分配 (base_size + 1) 集
            # 这样余数会被平摊到前几个组中
            current_batch_size = base_size + (1 if i < remainder else 0)
            end = start + current_batch_size
            
            batch = files[start:end]
            if batch:
                final_groups.append(batch)
            start = end
            
    return final_groups