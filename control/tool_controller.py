import threading
import os
from tkinter import messagebox
from logic.txt_logic import run_txt_merge_task
from logic.pdf_logic import run_pdf_merge_task
from logic.word_logic import run_win32_merge_task
from function.trash import clear_output_to_trash

class ToolController:
    def start_generic_task(self, task_func, log_callback=None):
        target = self.path_var.get().strip()
        if not target or not os.path.exists(target): 
            messagebox.showerror("错误", "请选择有效目录"); return
        
        final_log = log_callback if log_callback else self.log
        self.gui.progress.configure(progress_color="#28a745")
        self.gui.progress.set(0)

        threading.Thread(
            target=task_func, 
            args=(target, final_log, self.gui.progress, self.root), 
            kwargs={'output_dir': self.get_output_dir()}, 
            daemon=True
        ).start()
        
    def clean_script_trash(self):
        """点击清理按钮时触发"""
        target_dir = self.path_var.get().strip()
        if not target_dir or not os.path.exists(target_dir):
            messagebox.showwarning("提示", "请先选择有效的源目录")
            return
            
        # 调用工具
        clear_output_to_trash(target_dir, self.log)    

    def start_win32_thread(self): 
        self.start_generic_task(run_win32_merge_task, lambda m: self.log(m, tag="word_blue"))

    def start_pdf_merge_thread(self): 
        self.start_generic_task(run_pdf_merge_task, lambda m: self.log(m, tag="pdf_red"))

    def start_txt_merge_thread(self): 
        self.start_generic_task(run_txt_merge_task)