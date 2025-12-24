import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Frame, PageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics

# 引用全局配置的字体名
from config.settings import FONT_NAME_BODY, FONT_NAME_ENG

try:
    from pypdf import PdfWriter as PdfMerger 
except ImportError:
    PdfMerger = None

# --- 核心修改：按照拆分后的模块进行导入 ---
from function.paths import get_organized_path, get_save_path
from function.files import find_files_recursively, smart_group_files
from function.parsers import parse_subtitle_to_list
from function.naming import generate_output_name, clean_filename_title
# ---------------------------------------

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
        c.setFont(FONT_NAME_BODY, 9); c.setFillColor(colors.gray)
        page_width, page_height = self.pagesize
        c.drawCentredString(page_width / 2.0, page_height - 15 * mm, self.current_header_title)
        c.setStrokeColor(colors.lightgrey); c.setLineWidth(0.5)
        c.line(20*mm, page_height - 18*mm, page_width - 20*mm, page_height - 18*mm)
        c.restoreState()

def run_pdf_task(target_dir, log_func, progress_bar, root, batch_size=0, output_dir=None):
    log_func(f"[PDF生成] 扫描目录: {target_dir}")
    # 使用 files.py 的递归查找
    files = find_files_recursively(target_dir, ('.srt', '.vtt', '.ass'))
    if not files: return log_func("❌ 未找到字幕文件。")

    # 使用 files.py 的智能分组
    file_groups = smart_group_files(files, batch_size)
    total_files = len(files)
    processed_count = 0

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle('ChapterTitle', fontName=FONT_NAME_BODY, fontSize=16, leading=20, spaceAfter=10, textColor=colors.darkblue)
    toc_h = ParagraphStyle('TOCHeader', fontName=FONT_NAME_ENG, fontSize=20, alignment=TA_CENTER)
    body = ParagraphStyle('SubtitleBody', fontName=FONT_NAME_BODY, fontSize=10, leading=14, spaceAfter=4, alignment=TA_LEFT)

    # 路径逻辑适配：不要在此手动拼接 "script"
    base_output_dir = output_dir if output_dir else target_dir

    for group in file_groups:
        if not group: continue
        # 使用 naming.py 的命名
        out_name = generate_output_name([os.path.basename(f) for f in group], ".pdf")
        # 核心改动：get_organized_path 会识别 .pdf 并自动建立 script/pdf
        out_path = get_organized_path(base_output_dir, out_name)
        
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
                
                # 使用 parsers.py 的解析
                content_list = parse_subtitle_to_list(fp)
                if not content_list:
                    story.append(Paragraph("<i>[无对白]</i>", body))
                else:
                    for time_str, text in content_list:
                        safe_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        story.append(Paragraph(f"<b>[{time_str}]</b>  {safe_text}", body))
                
                processed_count += 1
                progress_bar.set(processed_count / total_files)
                root.update_idletasks()
            doc.multiBuild(story)
            log_func(f"📄 已生成: {os.path.join('script/pdf', out_name)}")
        except Exception as e: log_func(f"❌ 失败: {e}")
    progress_bar.set(0)

def run_pdf_merge_task(target_dir, log_func, progress_bar, root, output_dir=None):
    if PdfMerger is None: return log_func("❌ 缺少 pypdf 库，请安装。")
    
    log_func(f"扫描 PDF: {target_dir}")
    root_files = sorted([os.path.join(target_dir, f) for f in os.listdir(target_dir) 
                        if f.lower().endswith('.pdf') and "合并" not in f])
    
    target_files = root_files if root_files else []
    save_dir = target_dir

    if not target_files:
        # 适配新的分类层级：检测 script/pdf
        sub_dir = os.path.join(target_dir, "script", "pdf")
        if os.path.exists(sub_dir):
            target_files = sorted([os.path.join(sub_dir, f) for f in os.listdir(sub_dir) 
                                 if f.lower().endswith('.pdf') and "合并" not in f])
            save_dir = sub_dir

    if not target_files: return log_func("❌ 未找到 PDF 文件")

    merger = PdfMerger()
    try:
        for i, f in enumerate(target_files):
            log_func(f"合并中: {os.path.basename(f)}")
            merger.append(f)
            progress_bar.set((i + 1) / len(target_files))
            root.update_idletasks()
            
        out_path = os.path.join(save_dir, "PDF合并.pdf")
        merger.write(out_path)
        merger.close()
        log_func(f"✅ 合并成功: {out_path}")
    except Exception as e: log_func(f"❌ 错误: {e}")
    finally: progress_bar.set(0)