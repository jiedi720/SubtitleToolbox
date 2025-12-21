import os
import glob
import pysrt
import threading
from tkinter import messagebox
from docx.shared import Pt, RGBColor, Mm

# 尝试导入依赖
try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    import win32com.client as win32
    import pythoncom
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

# 尝试从 utils 导入
try:
    from utils import clean_filename_title, clean_subtitle_text_common, generate_output_name
except ImportError:
    # 后备逻辑
    def clean_filename_title(n): return os.path.splitext(n)[0]
    def clean_subtitle_text_common(t): return t.strip()
    def generate_output_name(files, ext): return "merged" + ext

def run_word_creation_task(target_dir, log_func, progress_bar, root):
    """
    任务1: 读取目录下所有 SRT，生成一个汇总的 Word 文档 (使用 python-docx)
    """
    if not HAS_DOCX:
        log_func("错误: 缺少 python-docx 库")
        return

    files = [f for f in os.listdir(target_dir) if f.lower().endswith('.srt')]
    files.sort()
    if not files:
        log_func("[Word] 未找到 SRT 文件。")
        return

    out_name = generate_output_name(files, ".docx")
    out_path = os.path.join(target_dir, out_name)
    
    doc = Document()
    for section in doc.sections:
        section.top_margin = Mm(25); section.bottom_margin = Mm(25)
        section.left_margin = Mm(25); section.right_margin = Mm(25)

    progress_bar["maximum"] = len(files)
    
    for i, fname in enumerate(files):
        dname = clean_filename_title(fname)
        log_func(f"[Word] 正在写入: {dname}")
        heading = doc.add_heading(dname, level=1)
        if heading.runs:
            run = heading.runs[0]
            run.font.color.rgb = RGBColor(0, 51, 102)

        try: subs = pysrt.open(os.path.join(target_dir, fname), encoding='utf-8')
        except: 
            try: subs = pysrt.open(os.path.join(target_dir, fname), encoding='gbk')
            except: subs = []

        for s in subs:
            txt = clean_subtitle_text_common(s.text)
            if not txt: continue
            
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            
            time_run = p.add_run(f"[{str(s.start)[:8]}]  ")
            time_run.bold = True; time_run.font.size = Pt(10)
            text_run = p.add_run(txt); text_run.font.size = Pt(10)

        if i < len(files)-1: doc.add_page_break()
        progress_bar["value"] = i + 1
        root.update_idletasks()
        
    doc.save(out_path)
    log_func(f"[SRT->Word] ✅ 剧本生成成功! 文件: {out_name}")

def run_win32_merge_task(target_dir, log_func, progress_bar, root):
    """
    任务2: 调用本地 Word 合并目录下的所有 .docx 文件
    """
    if not HAS_WIN32:
        messagebox.showerror("错误", "未安装 pywin32。\n请运行: pip install pywin32")
        return
        
    # 线程必须初始化 COM
    pythoncom.CoInitialize()
    
    log_func(f"[Word合并] 正在扫描目录: {target_dir}")
    
    all_files = glob.glob(os.path.join(target_dir, "*.docx"))
    # 排除临时文件和已合并文件
    files = [f for f in all_files if not os.path.basename(f).startswith("~$") and "全剧本" not in f and "merged" not in f]
    files.sort()
    
    if not files:
        log_func("[Word合并] 未找到待合并的 .docx 文件")
        pythoncom.CoUninitialize()
        return

    log_func("正在启动 Microsoft Word (后台运行)...")
    word = None
    try:
        word = win32.Dispatch('Word.Application')
        word.Visible = False
        word.DisplayAlerts = False
        
        new_doc = word.Documents.Add()
        selection = word.Selection
        
        total = len(files)
        log_func(f"共找到 {total} 个文件，开始合并...")
        progress_bar["maximum"] = total
        progress_bar["value"] = 0
        
        for index, file_path in enumerate(files):
            filename = os.path.basename(file_path)
            log_func(f"Processing [{index + 1}/{total}]: {filename}")
            
            selection.InsertFile(FileName=file_path, ConfirmConversions=False, Link=False, Attachment=False)
            
            if index < total - 1:
                selection.InsertBreak(Type=7) # 分页符
            
            progress_bar["value"] = index + 1
            root.update_idletasks()
            
        output_name = f"全剧本.docx"
        output_path = os.path.join(target_dir, output_name)
        
        new_doc.SaveAs2(output_path, FileFormat=12)
        new_doc.Close()
        
        log_func("-" * 30)
        # --- 修复点：这里原来写的是 out_name (未定义)，改为 output_name ---
        log_func(f"[Word合并] ✅ 成功! 输出文件: {output_name}")
        
    except Exception as e:
        log_func(f"❌ 错误: {e}")
        messagebox.showerror("Word 错误", str(e))
    finally:
        if word:
            try: word.Quit()
            except: pass
        pythoncom.CoUninitialize()
        progress_bar["value"] = 0