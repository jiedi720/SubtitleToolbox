import os
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

# --- 核心修改：按照拆分后的模块进行导入 ---
from function.paths import get_organized_path, get_save_path
from function.files import find_files_recursively, smart_group_files
from function.parsers import parse_subtitle_to_list
from function.naming import generate_output_name, clean_filename_title
# ---------------------------------------

def run_word_creation_task(target_dir, log_func, progress_bar, root, batch_size=0, output_dir=None):
    if not HAS_DOCX: return log_func("❌ 错误: 缺少 python-docx 库")
    
    log_func(f"[Word生成] 扫描: {target_dir}")
    # 使用 files.py 的递归查找
    files = find_files_recursively(target_dir, ('.srt', '.vtt', '.ass'))
    if not files: return log_func("❌ 未找到字幕。")

    # 使用 files.py 的智能分组
    file_groups = smart_group_files(files, batch_size)
    total_files = len(files)
    count = 0

    # 路径逻辑适配：不要在此手动拼接 "script"
    base_output_dir = output_dir if output_dir else target_dir

    for group in file_groups:
        if not group: continue
        # 使用 naming.py 的命名生成
        out_name = generate_output_name([os.path.basename(f) for f in group], ".docx")
        # 核心改动：get_organized_path 会识别 .docx 并自动创建 script/word
        out_path = get_organized_path(base_output_dir, out_name)
        
        try:
            doc = Document()
            for i, fp in enumerate(group):
                title_text = clean_filename_title(os.path.basename(fp))
                section = doc.sections[0] if i == 0 else doc.add_section()
                section.top_margin = section.bottom_margin = Mm(25)
                section.left_margin = section.right_margin = Mm(25)
                
                header_para = section.header.paragraphs[0]
                header_para.text = title_text
                header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

                doc.add_heading(title_text, level=1)
                
                # 使用 parsers.py 的解析器
                content_list = parse_subtitle_to_list(fp)
                
                if not content_list:
                    doc.add_paragraph("[无对白内容]")
                else:
                    for time_str, text in content_list:
                        p = doc.add_paragraph()
                        p.paragraph_format.space_after = Pt(4)
                        run = p.add_run(f"[{time_str}]  ")
                        run.bold = True
                        p.add_run(text)

                count += 1
                progress_bar.set(count / total_files)
                root.update_idletasks()
            
            doc.save(out_path)
            log_func(f"📄 已生成: {os.path.join('script/word', out_name)}")
        except Exception as e: log_func(f"❌ 失败: {e}")
    progress_bar.set(0)

def run_win32_merge_task(target_dir, log_func, progress_bar, root, output_dir=None):
    if not HAS_WIN32: return log_func("❌ 错误: 未安装 pywin32")
    pythoncom.CoInitialize()
    
    root_files = sorted([os.path.join(target_dir, f) for f in os.listdir(target_dir) 
                        if f.lower().endswith('.docx') and "~$" not in f and "合并" not in f])
    
    target_files = root_files if root_files else []
    save_dir = target_dir

    if not target_files:
        # 适配新的分类层级：检测 script/word
        sub_dir = os.path.join(target_dir, "script", "word")
        if os.path.exists(sub_dir):
            target_files = sorted([os.path.join(sub_dir, f) for f in os.listdir(sub_dir) 
                                 if f.lower().endswith('.docx') and "~$" not in f and "合并" not in f])
            save_dir = sub_dir

    if not target_files:
        pythoncom.CoUninitialize()
        return log_func("❌ 未找到 Word 文件")

    word = None
    try:
        word = win32.Dispatch('Word.Application')
        word.Visible = False
        new_doc = word.Documents.Add()
        sel = word.Selection
        
        for i, fp in enumerate(target_files):
            log_func(f"合并中: {os.path.basename(fp)}")
            sel.InsertFile(os.path.abspath(fp))
            if i < len(target_files)-1: sel.InsertBreak(Type=7)
            progress_bar.set((i + 1) / len(target_files))
            root.update_idletasks()
        
        out_path = os.path.join(save_dir, "Word合并.docx")
        new_doc.SaveAs2(os.path.abspath(out_path), FileFormat=12)
        new_doc.Close()
        log_func(f"✅ 合并完成: {out_path}")
    except Exception as e: log_func(f"❌ 运行错误: {e}")
    finally:
        if word: word.Quit()
        pythoncom.CoUninitialize()
        progress_bar.set(0)