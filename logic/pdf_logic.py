#PDF 逻辑文件

import os
import pysrt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Frame, PageTemplate, NextPageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from config import FONT_NAME_BODY, FONT_NAME_ENG
from utils import clean_filename_title, clean_subtitle_text_common, generate_output_name

# --- ReportLab 辅助类 ---
class Bookmark(Flowable):
    def __init__(self, key): Flowable.__init__(self); self.key = key
    def draw(self): self.canv.bookmarkPage(self.key)
    def wrap(self, w, h): return (0, 0)

class OutlineEntry(Flowable):
    def __init__(self, title, key): Flowable.__init__(self); self.title = title; self.key = key
    def draw(self): self.canv.addOutlineEntry(self.title, self.key, level=0, closed=True)
    def wrap(self, w, h): return (0, 0)

class TOCFinished(Flowable):
    def wrap(self, w, h): return (0, 0)
    def draw(self): pass

class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        SimpleDocTemplate.__init__(self, filename, **kw)
        self.page_offset = 0
    def afterFlowable(self, flowable):
        if isinstance(flowable, TOCFinished): self.page_offset = self.page
        if isinstance(flowable, Paragraph):
            text = flowable.getPlainText()
            if flowable.style.name == 'ChapterTitle':
                key = getattr(flowable, '_bookmarkName', None)
                pg = max(1, self.page - self.page_offset)
                self.notify('TOCEntry', (0, text, pg, key) if key else (0, text, pg))

def footer_content(canvas, doc):
    physical_pg = canvas.getPageNumber()
    offset = getattr(doc, 'page_offset', 0)
    pg = physical_pg - offset
    if pg > 0:
        canvas.saveState()
        canvas.setFont(FONT_NAME_ENG, 9)
        canvas.drawCentredString(A4[0]/2, 10*mm, str(pg))
        canvas.restoreState()

def run_pdf_task(target_dir, log_func, progress_bar, root):
    files = [f for f in os.listdir(target_dir) if f.lower().endswith('.srt')]
    files.sort()
    if not files:
        log_func("[PDF] 未找到 SRT 文件。")
        return

    out_name = generate_output_name(files, ".pdf")
    out_path = os.path.join(target_dir, out_name)
    
    doc = MyDocTemplate(out_path, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    
    doc.addPageTemplates([
        PageTemplate(id='TOC', frames=frame, onPage=lambda c,d: None),
        PageTemplate(id='Body', frames=frame, onPage=footer_content)
    ])
    
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle('ChapterTitle', parent=styles['Heading1'], fontName=FONT_NAME_BODY, fontSize=16, leading=20, spaceAfter=10, textColor=colors.darkblue)
    toc_h = ParagraphStyle('TOCHeader', parent=styles['Heading1'], fontName=FONT_NAME_ENG, fontSize=20, leading=22, spaceAfter=20, alignment=TA_CENTER)
    body = ParagraphStyle('SubtitleBody', parent=styles['Normal'], fontName=FONT_NAME_BODY, fontSize=10, leading=14, spaceAfter=4)
    
    story = [Bookmark("TOC"), OutlineEntry("Content", "TOC"), Paragraph("<b>Content</b>", toc_h)]
    toc = TableOfContents(); toc.dotsMinLevel = 0
    toc.levelStyles = [ParagraphStyle('TOC1', fontName=FONT_NAME_BODY, fontSize=12, leftIndent=20, firstLineIndent=-20, spaceBefore=5)]
    story.append(toc); story.append(TOCFinished()); story.append(NextPageTemplate('Body')); story.append(PageBreak())
    
    progress_bar["maximum"] = len(files)
    
    for i, fname in enumerate(files):
        dname = clean_filename_title(fname)
        key = f"CH_{i}"
        
        story.append(Bookmark(key))
        story.append(OutlineEntry(dname, key))
        p = Paragraph(dname, h1); p._bookmarkName = key
        story.append(p); story.append(Spacer(1, 10))
        
        try: subs = pysrt.open(os.path.join(target_dir, fname), encoding='utf-8')
        except: subs = pysrt.open(os.path.join(target_dir, fname), encoding='gbk')
        
        for s in subs:
            txt = clean_subtitle_text_common(s.text)
            if not txt: continue
            safe = txt.replace('<','&lt;').replace('>','&gt;')
            story.append(Paragraph(f"<b>[{str(s.start)[:8]}]</b>  {safe}", body))
        
        if i < len(files)-1: story.append(PageBreak())
        progress_bar["value"] = i + 1
        root.update_idletasks()
        
    doc.multiBuild(story)
    log_func(f"[PDF] 生成完毕: {out_name}")