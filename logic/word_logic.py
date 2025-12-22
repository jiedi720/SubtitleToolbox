import os
import glob
from docx.shared import Pt, RGBColor, Mm
# 导入对齐常量
from docx.enum.text import WD_ALIGN_PARAGRAPH

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

try: 
    from utils import (
        clean_filename_title, 
        generate_output_name, 
        get_save_path, 
        get_organized_path,
        smart_group_files, 
        find_files_recursively, 
        parse_subtitle_to_list 
    )
except ImportError: 
    pass

# ==============================================================================
# 任务 1: 字幕转 Word (页眉居中 + 分节控制)
# ==============================================================================
def run_word_creation_task(target_dir, log_func, progress_bar, root, batch_size=0, output_dir=None):
    if not HAS_DOCX: return log_func("❌ 错误: 缺少 python-docx 库")
    
    log_func(f"[Word] 扫描: {target_dir}")
    files = find_files_recursively(target_dir, ('.srt', '.vtt', '.ass'))
    if not files: return log_func("[Word] ❌ 未找到字幕文件。")

    if batch_size > 0: log_func(f"[SRT->Word] 分组模式: {batch_size} 集/组")
    
    file_groups = smart_group_files(files, batch_size)
    progress_bar["maximum"] = len(files)
    count = 0

    base_output_dir = output_dir if output_dir else os.path.join(target_dir, "script")

    for group in file_groups:
        if not group: continue
        out_name = generate_output_name([os.path.basename(f) for f in group], ".docx")
        out_path = get_organized_path(base_output_dir, out_name)
        
        log_func(f"生成中: {out_name}")
        
        try:
            doc = Document()
            
            for i, fp in enumerate(group):
                fname = os.path.basename(fp)
                title_text = clean_filename_title(fname)

                # 使用分节符 (Section) 代替分页符，以便每集有独立页眉
                if i == 0:
                    section = doc.sections[0]
                else:
                    section = doc.add_section()

                # 1. 设置页边距
                section.top_margin = section.bottom_margin = Mm(25)
                section.left_margin = section.right_margin = Mm(25)

                # 2. 设置页眉
                # 取消 "链接到前一节"，确保每集页眉不同
                section.header.is_linked_to_previous = False
                
                header_para = section.header.paragraphs[0]
                header_para.clear() 
                
                # 添加文字 (灰色，小号)
                run = header_para.add_run(title_text)
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(128, 128, 128) # 灰色
                
                # [修改] 设置为居中对齐 (CENTER = 1)
                header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

                # 3. 添加正文大标题
                heading = doc.add_heading(title_text, level=1)
                if heading.runs:
                    heading.runs[0].font.color.rgb = RGBColor(0, 51, 102) 
                
                # 4. 写入内容
                content_list = parse_subtitle_to_list(fp)
                
                if not content_list:
                    p = doc.add_paragraph("[无对白内容]")
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

    log_func(f"[SRT->Word] ✅ 完成！保存目录: {base_output_dir}\\word")
    progress_bar["value"] = 0

# ==============================================================================
# 任务 2: Word 合并 (Win32)
# ==============================================================================
def run_win32_merge_task(target_dir, log_func, progress_bar, root, output_dir=None):
    if not HAS_WIN32: return log_func("错误: 未安装 pywin32")
    pythoncom.CoInitialize()
    
    base_dir = output_dir if (output_dir and os.path.exists(output_dir)) else os.path.join(target_dir, "script")
    search_dir = os.path.join(base_dir, "word")
    if not os.path.exists(search_dir): search_dir = base_dir

    log_func(f"正在搜索 Word 文档: {search_dir}")
    files = sorted([f for f in glob.glob(os.path.join(search_dir, "*.docx")) if "~$" not in f and "全剧本" not in f])
    
    if not files: 
        log_func("[Word合并] 未找到 .docx 文件")
        return pythoncom.CoUninitialize()

    log_func("启动 Word 合并...")
    word = None
    try:
        word = win32.Dispatch('Word.Application')
        word.Visible = False; word.DisplayAlerts = False
        new_doc = word.Documents.Add(); sel = word.Selection
        progress_bar["maximum"] = len(files)
        
        for i, fp in enumerate(files):
            log_func(f"合并中: {os.path.basename(fp)}")
            sel.InsertFile(fp, ConfirmConversions=False, Link=False, Attachment=False)
            if i < len(files)-1: sel.InsertBreak(Type=7) 
            progress_bar["value"] = i + 1
            root.update_idletasks()
        
        out_name = "全剧本_Word合并.docx"
        out_path = os.path.join(search_dir, out_name)
        new_doc.SaveAs2(out_path, FileFormat=12)
        new_doc.Close()
        log_func(f"[Word合并] ✅ 成功: {out_path}")
    except Exception as e: log_func(f"❌ 错误: {e}")
    finally: 
        if word: 
            try: word.Quit() 
            except: pass
        pythoncom.CoUninitialize(); progress_bar["value"] = 0