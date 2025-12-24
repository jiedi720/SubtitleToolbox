#专门负责文件查找、扫描和分组

import os
import math
from function.naming import get_series_name

def find_files_recursively(root_dir, extensions, exclude_dirs=None):
    if exclude_dirs is None: 
        exclude_dirs = ['script', 'Script', 'output', 'Output', 'ass', 'Ass']
    found_files = []
    for root, dirs, filenames in os.walk(root_dir):
        for d in list(dirs):
            if d in exclude_dirs: 
                dirs.remove(d)
        for filename in filenames:
            if filename.lower().endswith(extensions):
                found_files.append(os.path.join(root, filename))
    return sorted(found_files)

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