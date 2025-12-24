import os
from tkinter import messagebox

try:
    from send2trash import send2trash
    HAS_SEND2TRASH = True
except ImportError:
    HAS_SEND2TRASH = False

def clear_output_to_trash(target_root, log_func):
    """
    智能清理：仅对具体被占用的文件名使用 error_red 标签。
    """
    if not HAS_SEND2TRASH:
        messagebox.showerror("缺少组件", "请安装：pip install send2trash")
        return

    # 定位 script 文件夹
    if os.path.basename(target_root).lower() == "script":
        script_dir = target_root
    else:
        script_dir = os.path.join(target_root, "script")

    if not os.path.exists(script_dir):
        log_func("[清理] ℹ️ 未发现 script 目录。")
        return

    try:
        items = os.listdir(script_dir)
    except Exception as e:
        log_func(f"❌ 无法读取目录: {e}")
        return

    if not items:
        log_func("[清理] ℹ️ 目录已空。")
        return

    if not messagebox.askyesno("确认清空", f"即将清空: {script_dir}\n确定吗？"):
        return

    deleted_total = 0
    error_total = 0

    for item in items:
        full_path = os.path.abspath(os.path.join(script_dir, item))
        
        try:
            send2trash(full_path)
            deleted_total += 1
        except Exception:
            if os.path.isdir(full_path):
                # 递归模式
                d, e = _recursive_delete(full_path, log_func)
                deleted_total += d
                error_total += e
            else:
                # 针对单个文件占用，仅在此处使用 error_red
                log_func(f"❌ 占用中: {item}", "error")
                error_total += 1

    # 汇总信息使用默认颜色
    if deleted_total > 0:
        log_func(f"✅ 已清理完成，共处理 {deleted_total} 个项目", "success")
    if error_total > 0:
        log_func(f"⚠️ 提示: 仍有 {error_total} 个文件未删除，请参考上方红字路径。")

def _recursive_delete(folder_path, log_func):
    """递归清理"""
    d_count = 0
    e_count = 0
    
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_p = os.path.join(root, name)
            try:
                send2trash(os.path.abspath(file_p))
                d_count += 1
            except Exception:
                # 核心改动：仅对该行报错使用 error_red
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
                
    return d_count, e_count