import os
import sys
import pysrt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Frame, PageTemplate, NextPageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# 字体处理依赖
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 尝试从 utils 导入
try:
    from utils import clean_filename_title, clean_subtitle_text_common, generate_output_name
except ImportError:
    # 后备逻辑
    def clean_filename_title(n): return os.path.splitext(n)[0]
    def clean_subtitle_text_common(t): return t.strip()
    def generate_output_name(f, e): return "merged" + e

# --- 1. 字体注册 (回归简单暴力版) ---
def register_fonts():
    """
    优先注册韩文/中文字体，防止乱码。
    """
    font_name = "CustomFont"
    
    # Windows 默认字体目录
    win_font_dir = r"C:\Windows\Fonts"
    
    # 候选列表：优先 Malgun (韩文支持最好), 其次 微软雅黑 (TTF版), 最后 黑体
    # 注意：ReportLab 对 .ttc (字体集) 支持不好，尽量用 .ttf
    candidates = ["malgun.ttf", "msyh.ttf", "simhei.ttf", "arialuni.ttf"]
    
    selected_path = None
    
    for filename in candidates:
        path = os.path.join(win_font_dir, filename)
        if os.path.exists(path):
            try:
                # 尝试注册
                pdfmetrics.registerFont(TTFont(font_name, path))
                # 如果成功，就用这个
                return font_name, "Helvetica"
            except Exception:
                continue
                
    # 如果都失败，返回 Helvetica (会乱码，但在控制台打印警告)
    print("⚠️ 严重警告: 未能加载任何中韩文字体！")
    return "Helvetica", "Helvetica"

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
        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(A4[0]/2, 10*mm, str(pg))
        canvas.restoreState()

# --- 2. 核心生成逻辑 ---
def run_pdf_task(target_dir, log_func, progress_bar, root):
    """
    生成 PDF，严格保持台词分行，不合并段落。
    """
    # 注册字体
    FONT_NAME_BODY, FONT_NAME_ENG = register_fonts()
    
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
    
    h1 = ParagraphStyle(
        'ChapterTitle', 
        parent=styles['Heading1'], 
        fontName=FONT_NAME_BODY, 
        fontSize=16, 
        leading=20, 
        spaceAfter=10, 
        textColor=colors.darkblue
    )
    
    toc_h = ParagraphStyle(
        'TOCHeader', 
        parent=styles['Heading1'], 
        fontName=FONT_NAME_ENG, 
        fontSize=20, 
        leading=22, 
        spaceAfter=20, 
        alignment=TA_CENTER
    )
    
    # 正文样式：左对齐，段后距设为 4，保证每句台词分开
    body = ParagraphStyle(
        'SubtitleBody', 
        parent=styles['Normal'], 
        fontName=FONT_NAME_BODY, 
        fontSize=10, 
        leading=14, 
        spaceAfter=4, 
        alignment=TA_LEFT
    )
    
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
        except: 
            try: subs = pysrt.open(os.path.join(target_dir, fname), encoding='gbk')
            except: subs = []
        
        # --- 逐行写入逻辑 ---
        for s in subs:
            txt = clean_subtitle_text_common(s.text)
            if not txt: continue
            
            # HTML 安全转义
            safe_txt = txt.replace('&', '&amp;').replace('<','&lt;').replace('>','&gt;')
            
            # 获取时间戳 [00:00:25]
            time_str = str(s.start)[:8]
            
            # 直接创建段落，确保不乱码，不合并
            line_content = f"<b>[{time_str}]</b>&nbsp;&nbsp;{safe_txt}"
            story.append(Paragraph(line_content, body))
        
        if i < len(files)-1: story.append(PageBreak())
        progress_bar["value"] = i + 1
        root.update_idletasks()
        
    log_func(f"[PDF] 正在渲染页面，请稍候...")
    try:
        doc.multiBuild(story)
        log_func(f"[SRT->PDF] ✅ 剧本生成成功! 文件: {out_name}")
    except Exception as e:
        log_func(f"❌ PDF 生成失败: {e}")
        if "Permission denied" in str(e):
            log_func("⚠️ 请先关闭已打开的 PDF 文件！")

# PDF 合并逻辑
def run_pdf_merge_task(target_dir, log_func, progress_bar, root):
    files = [f for f in os.listdir(target_dir) if f.lower().endswith('.pdf') and not f.startswith("Merged_")]
    files.sort()
    
    if not files:
        log_func("[PDF合并] 未找到 PDF 文件 (已忽略以 Merged_ 开头的文件)。")
        return

    log_func(f"[PDF合并] 发现 {len(files)} 个文件，准备合并...")

    try:
        try:
            from pypdf import PdfWriter, PdfReader
        except ImportError:
            from PyPDF2 import PdfWriter, PdfReader
    except ImportError:
        log_func("[错误] 缺少 PDF 库，请运行: pip install pypdf")
        return

    merger = PdfWriter()
    progress_bar["maximum"] = len(files)

    try:
        for i, pdf in enumerate(files):
            path = os.path.join(target_dir, pdf)
            merger.append(path)
            progress_bar["value"] = i + 1
            root.update_idletasks()
        
        out_name = os.path.join(target_dir, "全剧本.pdf")
        with open(out_name, "wb") as f_out:
            merger.write(f_out)
        
        log_func(f"[PDF合并] ✅ 成功! 输出文件: {os.path.basename(out_name)}")
        
    except Exception as e:
        log_func(f"[PDF合并] ❌ 失败: {str(e)}")
    finally:
        merger.close()
        progress_bar["value"] = 0