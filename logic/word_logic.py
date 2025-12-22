import os
import glob
import pythoncom
from docx.shared import Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH

try: 
    from docx import Document
    HAS_DOCX = True
except ImportError: 
    HAS_DOCX = False

try: 
    import win32com.client as win32
    HAS_WIN32 = True
except ImportError: 
    HAS_WIN32 = False

try: 
    from utils import (
        clean_filename_title, 
        generate_output_name, 
        get_organized_path,
        smart_group_files, 
        find_files_recursively, 
        parse_subtitle_to_list 
    )
except ImportError: 
    pass

# ==============================================================================
# 任务 1: 字幕转 Word (生成任务，保留 script 逻辑)
# ==============================================================================
def run_word_creation_task(target_dir, log_func, progress_bar, root, batch_size=0, output_dir=None):
    if not HAS_DOCX: return log_func("❌ 错误: 缺少 python-docx 库")
    
    log_func(f"[Word生成] 扫描: {target_dir}")
    files = find_files_recursively(target_dir, ('.srt', '.vtt', '.ass'))
    if not files: return log_func("[Word] ❌ 未找到字幕文件。")

    batch_n = batch_size if batch_size > 0 else 0
    file_groups = smart_group_files(files, batch_n)
    progress_bar["maximum"] = len(files)
    count = 0

    # 生成任务依然存放在 script/word
    base_output_dir = output_dir if output_dir else os.path.join(target_dir, "script")

    for group in file_groups:
        if not group: continue
        out_name = generate_output_name([os.path.basename(f) for f in group], ".docx")
        out_path = get_organized_path(base_output_dir, out_name)
        
        log_func(f"正在生成: {out_name}")
        
        try:
            doc = Document()
            for i, fp in enumerate(group):
                fname = os.path.basename(fp)
                title_text = clean_filename_title(fname)

                if i == 0:
                    section = doc.sections[0]
                else:
                    section = doc.add_section()

                section.top_margin = section.bottom_margin = Mm(25)
                section.left_margin = section.right_margin = Mm(25)
                section.header.is_linked_to_previous = False
                
                header_para = section.header.paragraphs[0]
                header_para.clear() 
                run = header_para.add_run(title_text)
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(128, 128, 128)
                header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

                heading = doc.add_heading(title_text, level=1)
                if heading.runs:
                    heading.runs[0].font.color.rgb = RGBColor(0, 51, 102) 
                
                content_list = parse_subtitle_to_list(fp)
                if not content_list:
                    doc.add_paragraph("[无对白内容]")
                else:
                    for time_str, text in content_list:
                        p = doc.add_paragraph()
                        p.paragraph_format.space_after = Pt(4)
                        r1 = p.add_run(f"[{time_str}]  ")
                        r1.bold = True
                        r1.font.size = Pt(10)
                        r2 = p.add_run(text)
                        r2.font.size = Pt(10)

                count += 1
                progress_bar["value"] = count
                root.update_idletasks()

            doc.save(out_path)
        except Exception as e: 
            log_func(f"❌ 保存失败 {out_name}: {e}")

    log_func(f"[Word生成] ✅ 完成！保存至: {base_output_dir}\\word")
    progress_bar["value"] = 0

# ==============================================================================
# 任务 2: Word 合并 (合并任务，忽略 script，直接找 word 文件夹)
# ==============================================================================
def run_win32_merge_task(target_dir, log_func, progress_bar, root, output_dir=None):
    if not HAS_WIN32: return log_func("错误: 未安装 pywin32")
    pythoncom.CoInitialize()
    
    # 【核心逻辑修改】直接查找选定目录下的 word 子文件夹
    search_dir = os.path.join(target_dir, "word")
    
    if not os.path.exists(search_dir):
        return log_func(f"❌ 未找到待合并目录: {search_dir}")

    log_func(f"正在扫描 Word 文档: {search_dir}")
    
    # 获取所有 docx，放宽限制
    files = sorted([
        os.path.join(search_dir, f) for f in os.listdir(search_dir) 
        if f.lower().endswith('.docx') 
        and "~$" not in f 
        and "全剧本" not in f
    ])
    
    if not files: 
        log_func("❌ 该目录下未找到待合并的 .docx 文件")
        return pythoncom.CoUninitialize()

    log_func(f"启动合并 (共 {len(files)} 个文件)...")
    word = None
    try:
        word = win32.Dispatch('Word.Application')
        word.Visible = False
        word.DisplayAlerts = False
        new_doc = word.Documents.Add()
        sel = word.Selection
        
        progress_bar["maximum"] = len(files)
        
        for i, fp in enumerate(files):
            log_func(f"合并中: {os.path.basename(fp)}")
            # 使用绝对路径以确保 win32com 正确识别
            abs_path = os.path.abspath(fp)
            sel.InsertFile(abs_path, ConfirmConversions=False, Link=False, Attachment=False)
            
            if i < len(files) - 1: 
                sel.InsertBreak(Type=7) # 分页符
                
            progress_bar["value"] = i + 1
            root.update_idletasks()
        
        out_name = "全剧本_Word合并.docx"
        out_path = os.path.join(search_dir, out_name)
        new_doc.SaveAs2(os.path.abspath(out_path), FileFormat=12)
        new_doc.Close()
        log_func(f"✅ 合并成功！文件位于: {out_path}")
        
    except Exception as e: 
        log_func(f"❌ 运行错误: {e}")
    finally: 
        if word: 
            try: word.Quit() 
            except: pass
        pythoncom.CoUninitialize()
        progress_bar["value"] = 0