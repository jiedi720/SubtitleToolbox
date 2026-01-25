"""
分卷逻辑处理模块
负责处理文件的智能分组、分卷设置管理等功能。
"""

import os
import math
from function.naming import get_series_name

__all__ = [
    'smart_group_files',
    'get_volume_pattern_setting',
    'get_batch_size_from_volume_pattern',
    'init_volume_settings',
    'load_volume_settings',
    'save_volume_settings'
]

def smart_group_files(file_paths, max_batch_size):
    """智能分组逻辑：保证每个分卷的集数尽可能平均
    
    例如：10集限制最大4集时，会分成 4+3+3；6集限制4集时，会分成 3+3。
    
    Args:
        file_paths: 文件路径列表
        max_batch_size: 每组最大文件数（0表示整季模式，按剧集分组）
        
    Returns:
        list: 分组后的文件列表，每个元素是一组文件路径
    """
    if not file_paths: return []
    
    import re
    
    files = sorted(file_paths)
    total = len(files)
    final_groups = []
    
    # 如果不限制每包大小（整季模式），则按剧集名称分组
    if max_batch_size <= 0:
        # 按剧集名称和季号分组，确保不同季分别保存
        series_season_groups = {}
        pattern_se = re.compile(r'[Ss](\d{1,2})[\s.]*[Ee](\d{1,3})', re.IGNORECASE)
        
        for fp in files:
            filename = os.path.basename(fp)
            
            # 提取季号
            match = pattern_se.search(filename)
            if match:
                # 有集数标识的文件：按系列名和季号分组
                series_name = get_series_name(filename)
                season_num = match.group(1)
                # 使用"系列名+S季号"作为分组键
                group_key = f"{series_name}_S{season_num}"
                
                if group_key not in series_season_groups:
                    series_season_groups[group_key] = []
                series_season_groups[group_key].append(fp)
            else:
                # 没有季号的文件：每个文件单独分组
                # 新闻类或其他没有集数标识的文件应该单独处理
                final_groups.append([fp])
        
        # 将有集数标识的文件分组添加到最终结果
        sorted_keys = sorted(series_season_groups.keys())
        for key in sorted_keys:
            if series_season_groups[key]:
                final_groups.append(series_season_groups[key])
        
        return final_groups
    
    # 核心平摊算法（智能模式和单集模式）
    # 1. 计算总共需要分成几个组
    num_groups = math.ceil(total / max_batch_size)
    
    # 2. 计算每组的基础大小和多出来的余数
    base_size = total // num_groups
    remainder = total % num_groups
    
    # 3. 分配文件到各组
    start = 0
    for i in range(num_groups):
        # 如果当前组的索引小于余数，则该组分配 (base_size + 1) 集
        current_batch_size = base_size + (1 if i < remainder else 0)
        end = start + current_batch_size
        
        batch = files[start:end]
        if batch:
            final_groups.append(batch)
        start = end
        
    return final_groups


def get_volume_pattern_setting(volume_pattern):
    """根据分卷模式获取对应的设置
    
    Args:
        volume_pattern: 分卷模式（"整季"、"智能"、"单集"）
        
    Returns:
        int: 对应的每组最大文件数
    """
    # 映射分卷模式到最大集数
    mode_map = {
        "整季": 0,  # 0表示整季不分卷
        "智能": 4,  # 智能模式，每卷最多4集
        "单集": 1   # 单集模式，每卷1集
    }
    return mode_map.get(volume_pattern, 0)


def get_batch_size_from_volume_pattern(volume_pattern):
    """根据分卷模式获取对应的batch_size
    
    Args:
        volume_pattern: 分卷模式（"整季"、"智能"、"单集"）
        
    Returns:
        int: 对应的batch_size值
    """
    return get_volume_pattern_setting(volume_pattern)


def init_volume_settings():
    """初始化分卷相关设置
    
    Returns:
        dict: 初始化的分卷设置字典
    """
    return {
        "volume_pattern": "整季"
    }


def load_volume_settings(config_gen):
    """从配置文件加载分卷相关设置
    
    Args:
        config_gen: 配置生成器或字典
        
    Returns:
        dict: 加载的分卷设置字典
    """
    return {
        "volume_pattern": config_gen.get("volume_pattern", "整季")
    }


def save_volume_settings(volume_settings):
    """准备分卷相关设置用于保存到配置文件
    
    Args:
        volume_settings: 分卷设置字典
        
    Returns:
        dict: 格式化后的配置字典，适合保存到文件
    """
    return {
        "volume_pattern": volume_settings["volume_pattern"]
    }
