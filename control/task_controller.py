import os
import threading
from tkinter import messagebox
from logic.txt_logic import run_txt_creation_task
from logic.pdf_logic import run_pdf_task
from logic.word_logic import run_word_creation_task
from font.ass import run_ass_task

class TaskController:
    def start_thread(self): 
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        target_dir = self.path_var.get().strip()
        if not target_dir or not os.path.exists(target_dir):
            messagebox.showerror("错误", "源目录无效"); return
        
        final_out = self.get_output_dir()
        if not os.path.exists(final_out): os.makedirs(final_out, exist_ok=True)
            
        self.gui.app.start_btn.configure(state='disabled')
        self.gui.progress.set(0)
        self.gui.progress.configure(progress_color="#28a745")
        
        self.log(f"--- 任务启动 ---")
        try:
            mode = self.task_mode.get()
            if mode == "ASS":
                run_ass_task(target_dir, self._get_current_styles(), self.log, self.gui.progress, self.root, output_dir=final_out)
            elif mode == "PDF":
                batch = 4 if self.enable_grouping.get() else 0
                if self.do_pdf.get():
                    run_pdf_task(target_dir, lambda m: self.log(m, "pdf_red"), self.gui.progress, self.root, batch, final_out)
                if self.do_word.get():
                    run_word_creation_task(target_dir, lambda m: self.log(m, "word_blue"), self.gui.progress, self.root, batch, final_out)
                if self.do_txt.get():
                    run_txt_creation_task(target_dir, self.log, self.gui.progress, self.root, batch, final_out)
            self.log("✅ 任务流处理完毕。")
        except Exception as e: self.log(f"❌ 出错: {e}")
        finally:
            self.gui.app.start_btn.configure(state='normal')
            self.gui.progress.configure(progress_color=("#CCCCCC", "#3d3d3d"))

    def _get_current_styles(self):
        if hasattr(self, 'kor_panel_ui'):
            k = self.construct_style_line(self.kor_parsed["raw"], self.kor_panel_ui, "KOR")
            c = self.construct_style_line(self.chn_parsed["raw"], self.chn_panel_ui, "CHN")
            return {"kor": k, "chn": c}
        return {"kor": self.kor_parsed["raw"], "chn": self.chn_parsed["raw"]}