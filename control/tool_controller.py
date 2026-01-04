import threading
import os
from PySide6.QtWidgets import QMessageBox
from function.merge import run_txt_merge_task, run_pdf_merge_task, run_win32_merge_task
from function.trash import clear_output_to_trash


class ToolController:
    """
    工具控制器类，负责处理各种工具任务，如合并任务和清理任务
    """
    
    def start_generic_task(self, task_func, log_callback=None):
        """
        启动通用任务
        
        Args:
            task_func: 要执行的任务函数
            log_callback: 日志回调函数（可选）
        """
        # 获取目标目录
        target = self.path_var.strip()
        if not target or not os.path.exists(target): 
            QMessageBox.critical(None, "错误", "请选择有效目录")
            return
        
        # 设置日志回调
        final_log = log_callback if log_callback else self.log
        
        # 更新进度条
        if hasattr(self.gui, 'ProgressBar'):
            self.gui.ProgressBar.setValue(0)

        # 启动任务线程
        threading.Thread(
            target=task_func, 
            args=(target, final_log, self.update_progress, self.root), 
            kwargs={'output_dir': self.output_path_var.strip()}, 
            daemon=True
        ).start()
        
