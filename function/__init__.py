"""
功能模块统一导入接口
集中管理所有功能函数的导入，提供统一的访问接口
"""

# 文件处理相关
from .file_utils import find_files_recursively, get_organized_path, get_save_path

# 字幕解析与清洗相关
from .parsers import parse_subtitle_to_list, clean_subtitle_text_common, clean_subtitle_text_ass

# 分卷逻辑相关
from .volumes import (
    smart_group_files,
    get_volume_pattern_setting,
    get_batch_size_from_volume_pattern,
    init_volume_settings,
    load_volume_settings,
    save_volume_settings
)

# 命名处理相关
from .naming import (
    clean_filename_title,
    get_series_name,
    generate_output_name
)

# 文件合并相关
from .merge import (
    run_pdf_merge_task,
    run_txt_merge_task,
    run_win32_merge_task
)

# 文件清理相关
from .trash import clear_output_to_trash

__all__ = [
    # 文件处理
    'find_files_recursively',
    'get_organized_path',
    'get_save_path',
    
    # 字幕解析与清洗
    'parse_subtitle_to_list',
    'clean_subtitle_text_common',
    'clean_subtitle_text_ass',
    
    # 分卷逻辑
    'smart_group_files',
    'get_volume_pattern_setting',
    'get_batch_size_from_volume_pattern',
    'init_volume_settings',
    'load_volume_settings',
    'save_volume_settings',
    
    # 命名处理
    'clean_filename_title',
    'get_series_name',
    'generate_output_name',
    
    # 文件合并
    'run_pdf_merge_task',
    'run_txt_merge_task',
    'run_win32_merge_task',
    
    # 文件清理
    'clear_output_to_trash'
]