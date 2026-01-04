"""
文件清理模块
负责将文件发送到回收站，提供智能清理功能，永远不会删除.srt原始文件。
"""

import os
from PySide6.QtWidgets import QMessageBox

__all__ = [
    'clear_output_to_trash'
]

try:
    from send2trash import send2trash
    HAS_SEND2TRASH = True
except ImportError:
    HAS_SEND2TRASH = False

def clear_output_to_trash(target_root, log_func):
    """智能清理输出目录，将文件发送到回收站
    
    注意：永远不会删除 .srt 原始文件，仅对被占用的文件名使用错误标签。
    
    Args:
        target_root: 目标根目录
        log_func: 日志记录函数
    """
    if not HAS_SEND2TRASH:
        QMessageBox.critical(None, "缺少组件", "请安装：pip install send2trash")
        return

    # 直接处理目标目录，不再寻找script文件夹
    cleanup_dir = target_root

    if not os.path.exists(cleanup_dir):
        log_func("[清理] ℹ️ 目录不存在。")
        return

    try:
        items = os.listdir(cleanup_dir)
    except Exception as e:
        log_func(f"❌ 无法读取目录: {e}")
        return

    if not items:
        log_func("[清理] ℹ️ 目录已空。")
        return

    if not QMessageBox.question(None, "确认清空", f"即将清空: {cleanup_dir}\n确定吗？", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
        return

    deleted_total = 0
    error_total = 0
    deleted_items = []  # 记录具体清理的项目

    for item in items:
        full_path = os.path.abspath(os.path.join(cleanup_dir, item))
        
        # 永远不会删除 .srt 原始文件
        if item.lower().endswith('.srt'):
            continue
            
        try:
            if os.path.isdir(full_path):
                # 递归清理文件夹，确保不会删除.srt文件
                d, e, recursive_items = _recursive_delete(full_path, log_func)
                deleted_total += d
                error_total += e
                # 保存完整路径的相对形式，显示更清晰
                for recursive_item in recursive_items:
                    full_item_path = os.path.join(item, recursive_item)
                    deleted_items.append(full_item_path)
                # 删除空文件夹
                try:
                    send2trash(full_path)
                    deleted_total += 1
                    deleted_items.append(item)
                except Exception:
                    # 文件夹可能不是空的，或者有其他问题，忽略
                    pass
            else:
                # 删除单个文件
                send2trash(full_path)
                deleted_total += 1
                deleted_items.append(item)
        except Exception:
            # 针对单个文件占用，使用错误标签
            log_func(f"❌ 占用中: {item}", "error")
            error_total += 1

    # 汇总信息
    if deleted_total > 0:
        log_func(f"✅ 已清理完成，共处理 {deleted_total} 个项目", "success")
        # 列出具体清理的项目
        log_func("[清理] 已清理的项目:")
        for item in deleted_items:
            log_func(f"  - {item}")
    if error_total > 0:
        log_func(f"⚠️ 提示: 仍有 {error_total} 个文件未删除，请参考上方红字路径。")

def _recursive_delete(folder_path, log_func):
    """递归清理文件夹，将文件发送到回收站
    
    Args:
        folder_path: 文件夹路径
        log_func: 日志记录函数
        
    Returns:
        tuple: (删除成功数量, 删除失败数量, 已删除项目列表)
    """
    d_count = 0
    e_count = 0
    deleted_items = []
    
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_p = os.path.join(root, name)
            # 永远不会删除 .srt 原始文件
            if name.lower().endswith('.srt'):
                continue
            
            try:
                send2trash(os.path.abspath(file_p))
                d_count += 1
                # 保存相对路径，显示更清晰
                relative_path = os.path.relpath(file_p, folder_path)
                deleted_items.append(relative_path)
            except Exception:
                # 仅对该行报错使用错误标签
                relative_path = os.path.join(os.path.basename(root), name)
                log_func(f"❌ 占用中: {relative_path}", "error")
                e_count += 1
        
        for name in dirs:
            dir_p = os.path.join(root, name)
            try:
                if not os.listdir(dir_p):
                    os.rmdir(dir_p)
            except:
                pass
                
    return d_count, e_count, deleted_items