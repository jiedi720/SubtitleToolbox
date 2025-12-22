import os
import glob
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Frame, PageTemplate, NextPageTemplate
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
        clean_filename_title, 
        generate_output_name, 
        get_save_path, 
        get_organized_path,
        smart_group_files, 
        find_files_recursively, 
        parse_subtitle_to_list 
    )
except ImportError: pass

# ==============================================================================
# 字体注册
# ==============================================================================
def register_fonts():
    candidates = ["malgun.ttf", "msyh.ttf", "simhei.ttf", "arialuni.ttf", "NotoSansCJKsc-Regular.otf"]
    for f in candidates:
        p = os.path.join(r"C:\Windows\Fonts", f)
        if os.path.exists(p):
            try: 
                pdfmetrics.registerFont(TTFont("CustomFont", p))
                return "CustomFont", "Helvetica"
            except: continue
    
    local_font = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "fonts", "NotoSansSC-Regular.ttf")
    if os.path.exists(local_font):
        try:
            pdfmetrics.registerFont(TTFont("CustomFont", local_font))
            return "CustomFont", "Helvetica"
        except: pass

    return "Helvetica", "Helvetica"

# ==============================================================================
# 自定义 Flowables
# ==============================================================================
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

# [核心修复] 用于更新文档标题的 Flowable
class SetHeaderTitle(Flowable):
    def __init__(self, title):
        Flowable.__init__(self)
        self.title = title
    
    def wrap(self, w, h): 
        return (0, 0)
        
    def draw(self):
        # 直接修改文档模板实例的属性
        if hasattr(self.canv, '_doctemplate'):
            self.canv._doctemplate.current_header_title = self.title

# ==============================================================================
# [核心修复] 重写 DocTemplate，利用 handle_pageBegin 强制绘制页眉
# ==============================================================================
class DynamicHeaderDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        SimpleDocTemplate.__init__(self, filename, **kw)
        self.current_header_title = None # 初始为空，目录页不显示

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'ChapterTitle':
            key = getattr(flowable, '_bookmarkName', None)
            if key:
                self.notify('TOCEntry', (0, flowable.getPlainText(), self.page, key))

    def handle_pageBegin(self):
        # 调用父类处理
        super().handle_pageBegin()
        # 在每一页开始时绘制页眉
        self._draw_custom_header()

    def _draw_custom_header(self):
        # 如果当前没有设置标题（如目录页），则不绘制
        if not self.current_header_title:
            return

        c = self.canv
        c.saveState()
        
        # 字体回退
        font_list = pdfmetrics.getRegisteredFontNames()
        font_name = "CustomFont" if "CustomFont" in font_list else "Helvetica"
        
        c.setFont(font_name, 9)
        c.setFillColor(colors.gray)
        
        # 居中绘制页眉
        page_width, page_height = self.pagesize
        c.drawCentredString(page_width / 2.0, page_height - 15 * mm, self.current_header_title)
        
        # 绘制分割线
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(0.5)
        c.line(20*mm, page_height - 18*mm, page_width - 20*mm, page_height - 18*mm)
        
        c.restoreState()

# ==============================================================================
# 任务 1: 生成 PDF
# ==============================================================================
def run_pdf_task(target_dir, log_func, progress_bar, root, batch_size=0, output_dir=None):
    FONT_BODY, FONT_ENG = register_fonts()
    
    log_func(f"[PDF] 扫描: {target_dir}")
    files = find_files_recursively(target_dir, ('.srt', '.vtt', '.ass'))
    if not files: return log_func("[PDF] ❌ 未找到字幕文件。")

    if batch_size > 0: log_func(f"[SRT->PDF] 分组模式: {batch_size} 集/组")
    file_groups = smart_group_files(files, batch_size)
    progress_bar["maximum"] = len(files)
    processed_count = 0

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle('ChapterTitle', parent=styles['Heading1'], fontName=FONT_BODY, fontSize=16, leading=20, spaceAfter=10, textColor=colors.darkblue)
    toc_h = ParagraphStyle('TOCHeader', parent=styles['Heading1'], fontName=FONT_ENG, fontSize=20, alignment=TA_CENTER)
    body = ParagraphStyle('SubtitleBody', parent=styles['Normal'], fontName=FONT_BODY, fontSize=10, leading=14, spaceAfter=4, alignment=TA_LEFT)

    base_output_dir = output_dir if output_dir else os.path.join(target_dir, "script")

    for group in file_groups:
        if not group: continue
        basenames = [os.path.basename(f) for f in group]
        out_name = generate_output_name(basenames, ".pdf")
        out_path = get_organized_path(base_output_dir, out_name)
        
        log_func(f"生成中: {out_name}")
        
        try:
            # 使用自定义的 DocTemplate
            doc = DynamicHeaderDocTemplate(out_path, pagesize=A4, topMargin=25*mm, bottomMargin=25*mm, leftMargin=25*mm, rightMargin=25*mm)
            
            # 使用最简单的 Frame，不需要在 PageTemplate 里绑定页眉函数了，因为 handle_pageBegin 会自动处理
            frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
            doc.addPageTemplates([PageTemplate(id='normal', frames=frame)])
            
            story = [
                Bookmark("TOC"), OutlineEntry("Content", "TOC"), 
                Paragraph("<b>Content</b>", toc_h), TableOfContents(), TOCFinished(), 
                PageBreak()
            ]
            
            for i, fp in enumerate(group):
                clean_title = clean_filename_title(os.path.basename(fp))
                key = f"CH_{processed_count}"
                
                # [关键逻辑]
                # 1. 设置标题 (这会立即更新 doc.current_header_title)
                # 2. 如果不是第一集，强制换页 (新页面开始时 handle_pageBegin 会读到新标题)
                story.append(SetHeaderTitle(clean_title))
                
                if i > 0:
                    story.append(PageBreak())

                # 章节标题
                p = Paragraph(clean_title, h1)
                p._bookmarkName = key
                story.extend([Bookmark(key), OutlineEntry(clean_title, key), p, Spacer(1, 10)])
                
                content_list = parse_subtitle_to_list(fp)
                if not content_list:
                    story.append(Paragraph("<i>[无对白内容]</i>", body))
                else:
                    for time_str, text in content_list:
                        safe_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        story.append(Paragraph(f"<b>[{time_str}]</b>  {safe_text}", body))
                
                processed_count += 1
                progress_bar["value"] = processed_count
                root.update_idletasks()
            
            doc.multiBuild(story)
            
        except Exception as e: 
            log_func(f"❌ 生成失败: {e}")

    log_func(f"[SRT->PDF] ✅ 完成！保存目录: {base_output_dir}\\pdf")
    progress_bar["value"] = 0

# ==============================================================================
# 任务 2: 合并 PDF (保持不变)
# ==============================================================================
def run_pdf_merge_task(target_dir, log_func, progress_bar, root, output_dir=None):
    if PdfMerger is None: return log_func("错误: 缺 pypdf")
    
    base_dir = output_dir if (output_dir and os.path.exists(output_dir)) else os.path.join(target_dir, "script")
    search_dir = os.path.join(base_dir, "pdf")
    if not os.path.exists(search_dir): search_dir = base_dir

    log_func(f"正在搜索 PDF: {search_dir}")
    files = sorted([f for f in glob.glob(os.path.join(search_dir, "*.pdf")) if "Merged_" not in f and "全剧本" not in f])
    
    if not files: return log_func("未找到 PDF")
    
    merger = PdfMerger()
    progress_bar["maximum"] = len(files)
    try:
        for i, f in enumerate(files):
            log_func(f"合并中: {os.path.basename(f)}")
            merger.append(f)
            progress_bar["value"] = i+1; root.update_idletasks()
        out_path = os.path.join(search_dir, "全剧本_PDF合并.pdf")
        merger.write(out_path); merger.close()
        log_func(f"✅ 合并成功: {out_path}")
    except Exception as e: log_func(f"❌ 错误: {e}")
    finally: progress_bar["value"] = 0