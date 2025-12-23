import os
import glob
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Frame, PageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

try: from pypdf import PdfWriter as PdfMerger 
except ImportError:
    try: from PyPDF2 import PdfMerger 
    except ImportError: PdfMerger = None

try: 
    from utils import (
        clean_filename_title, generate_output_name, get_save_path, 
        get_organized_path, smart_group_files, find_files_recursively, parse_subtitle_to_list 
    )
except ImportError: pass

# ... (register_fonts, Bookmark, OutlineEntry, TOCFinished, SetHeaderTitle, MyDocTemplate 保持不变) ...

def register_fonts():
    candidates = ["malgun.ttf", "msyh.ttf", "simhei.ttf", "arialuni.ttf", "NotoSansCJKsc-Regular.otf"]
    for f in candidates:
        p = os.path.join(r"C:\Windows\Fonts", f)
        if os.path.exists(p):
            try: 
                pdfmetrics.registerFont(TTFont("CustomFont", p))
                return "CustomFont", "Helvetica"
            except: continue
    return "Helvetica", "Helvetica"

class Bookmark(Flowable):
    def __init__(self, key): Flowable.__init__(self); self.key = key
    def draw(self): self.canv.bookmarkPage(self.key)
    def wrap(self, w, h): return (0, 0)

class OutlineEntry(Flowable):
    def __init__(self, t, k): Flowable.__init__(self); self.title=t; self.key=k
    def draw(self): self.canv.addOutlineEntry(self.title, self.key, level=0, closed=True)
    def wrap(self, w, h): return (0, 0)

class TOCFinished(Flowable):
    def wrap(self, w, h): return (0, 0)
    def draw(self): pass

class SetHeaderTitle(Flowable):
    def __init__(self, title):
        Flowable.__init__(self)
        self.title = title
    def wrap(self, w, h): return (0, 0)
    def draw(self):
        if hasattr(self.canv, '_doctemplate'):
            self.canv._doctemplate.current_header_title = self.title

class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        SimpleDocTemplate.__init__(self, filename, **kw)
        self.current_header_title = ""
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'ChapterTitle':
            key = getattr(flowable, '_bookmarkName', None)
            if key: self.notify('TOCEntry', (0, flowable.getPlainText(), self.page, key))
    def handle_pageBegin(self):
        super().handle_pageBegin()
        self._draw_custom_header()
    def _draw_custom_header(self):
        if not self.current_header_title: return
        c = self.canv
        c.saveState()
        font_name = "CustomFont" if "CustomFont" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
        c.setFont(font_name, 9); c.setFillColor(colors.gray)
        page_width, page_height = self.pagesize
        c.drawCentredString(page_width / 2.0, page_height - 15 * mm, self.current_header_title)
        c.setStrokeColor(colors.lightgrey); c.setLineWidth(0.5)
        c.line(20*mm, page_height - 18*mm, page_width - 20*mm, page_height - 18*mm)
        c.restoreState()

# ==============================================================================
# 任务 1: 从字幕生成 PDF (保留 script 逻辑)
# ==============================================================================
def run_pdf_task(target_dir, log_func, progress_bar, root, batch_size=0, output_dir=None):
    FONT_BODY, FONT_ENG = register_fonts()
    log_func(f"[PDF生成] 扫描: {target_dir}")
    files = find_files_recursively(target_dir, ('.srt', '.vtt', '.ass'))
    if not files: return log_func("[PDF] ❌ 未找到字幕文件。")

    batch_n = batch_size if batch_size > 0 else 0
    file_groups = smart_group_files(files, batch_n)
    progress_bar["maximum"] = len(files); processed_count = 0

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle('ChapterTitle', parent=styles['Heading1'], fontName=FONT_BODY, fontSize=16, leading=20, spaceAfter=10, textColor=colors.darkblue)
    toc_h = ParagraphStyle('TOCHeader', parent=styles['Heading1'], fontName=FONT_ENG, fontSize=20, alignment=TA_CENTER)
    body = ParagraphStyle('SubtitleBody', parent=styles['Normal'], fontName=FONT_BODY, fontSize=10, leading=14, spaceAfter=4, alignment=TA_LEFT)

    # 生成任务依然存放在 script/pdf
    base_output_dir = output_dir if output_dir else os.path.join(target_dir, "script")

    for group in file_groups:
        if not group: continue
        out_name = generate_output_name([os.path.basename(f) for f in group], ".pdf")
        out_path = get_organized_path(base_output_dir, out_name)
        log_func(f"正在生成: {out_name}")
        
        try:
            doc = MyDocTemplate(out_path, pagesize=A4, topMargin=25*mm, bottomMargin=25*mm, leftMargin=25*mm, rightMargin=25*mm)
            frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
            doc.addPageTemplates([PageTemplate(id='normal', frames=frame)])
            story = [Bookmark("TOC"), OutlineEntry("Content", "TOC"), Paragraph("<b>Content</b>", toc_h), TableOfContents(), TOCFinished(), PageBreak()]
            
            for i, fp in enumerate(group):
                clean_title = clean_filename_title(os.path.basename(fp))
                story.append(SetHeaderTitle(clean_title))
                if i > 0: story.append(PageBreak())
                p = Paragraph(clean_title, h1); p._bookmarkName = f"CH_{processed_count}"
                story.extend([Bookmark(p._bookmarkName), OutlineEntry(clean_title, p._bookmarkName), p, Spacer(1, 10)])
                
                content_list = parse_subtitle_to_list(fp)
                if not content_list: story.append(Paragraph("<i>[无对白]</i>", body))
                else:
                    for time_str, text in content_list:
                        safe_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        story.append(Paragraph(f"<b>[{time_str}]</b>  {safe_text}", body))
                processed_count += 1; progress_bar["value"] = processed_count; root.update_idletasks()
            doc.multiBuild(story)
        except Exception as e: log_func(f"❌ 失败: {e}")
    log_func(f"[PDF生成] ✅ 完成！保存至: {base_output_dir}\\pdf")
    progress_bar["value"] = 0

# ==============================================================================
# 任务 2: 合并 PDF（如果根目录有文件，就只处理根目录，不再看子文件夹）
# ==============================================================================

# ... (前面的生成逻辑 run_pdf_task 保持不变，它依然可以向 script 输出) ...

def run_pdf_merge_task(target_dir, log_func, progress_bar, root, output_dir=None):
    if PdfMerger is None: return log_func("错误: 缺少 pypdf 库")
    
    # 【彻底剥离 script】直接使用传入的 target_dir (源文件目录)
    log_func(f"检查根目录: {target_dir}")
    
    # 1. 优先级搜索：先看根目录
    root_files = sorted([os.path.join(target_dir, f) for f in os.listdir(target_dir) 
                        if f.lower().endswith('.pdf') and "全剧本" not in f and "Merged" not in f])
    
    target_files = []
    save_dir = target_dir

    if root_files:
        log_func(f"✨ 在根目录发现 {len(root_files)} 个 PDF。")
        target_files = root_files
    else:
        # 2. 优先级搜索：根目录没找到，看 target_dir 下的 pdf 子目录
        sub_dir = os.path.join(target_dir, "pdf")
        if os.path.exists(sub_dir):
            log_func(f"根目录无文件，检查子目录: {sub_dir}")
            sub_files = sorted([os.path.join(sub_dir, f) for f in os.listdir(sub_dir) 
                               if f.lower().endswith('.pdf') and "全剧本" not in f and "Merged" not in f])
            if sub_files:
                log_func(f"✨ 在子目录发现 {len(sub_files)} 个 PDF。")
                target_files = sub_files
                save_dir = sub_dir

    if not target_files:
        return log_func("❌ 未找到待合并文件（已检查根目录及 pdf 文件夹）")

    # 3. 合并过程
    merger = PdfMerger()
    progress_bar["maximum"] = len(target_files)
    try:
        for i, f in enumerate(target_files):
            log_func(f"合并中: {os.path.basename(f)}")
            merger.append(f)
            progress_bar["value"] = i+1; root.update_idletasks()
            
        out_path = os.path.join(save_dir, "PDF合并.pdf")
        merger.write(out_path)
        merger.close()
        log_func(f"✅ 合并成功！文件位于: {out_path}")
    except Exception as e:
        log_func(f"❌ 错误: {e}")
    finally:
        progress_bar["value"] = 0