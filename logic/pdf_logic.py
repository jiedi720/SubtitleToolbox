"""
PDF文档生成与合并模块
负责将字幕文件转换为PDF文档，并提供PDF文档合并功能。
"""

import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Frame, PageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 字体常量定义 - 使用支持多语言的字体设置
FONT_NAME_BODY = "Helvetica"
FONT_NAME_ENG = "Helvetica"
FONT_NAME_KR = "Helvetica"

def init_fonts():
    """初始化PDF字体
    
    优先从项目font文件夹加载字体，然后尝试系统字体。
    支持中文（NotoSansSC）和韩语（NotoSansKR-Medium）。
    """
    global FONT_NAME_BODY, FONT_NAME_ENG, FONT_NAME_KR
    
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_dir = os.path.join(project_root, 'font')
    
    # 尝试加载Noto Sans SC（简体中文）
    sc_fonts = [
        os.path.join(font_dir, 'NotoSansSC-Regular.ttf'),  # 项目字体文件夹
        os.path.join(font_dir, 'NotoSansSC-VF.ttf'),       # 项目字体文件夹
        "C:\\Windows\\Fonts\\NotoSansSC-Regular.ttf",      # 系统字体
        "C:\\Windows\\Fonts\\NotoSansSC-VF.ttf",           # 系统字体
        "C:\\Windows\\Fonts\\msyh.ttc",                    # 微软雅黑作为备用
    ]
    
    for font_path in sc_fonts:
        try:
            if os.path.exists(font_path):
                if font_path.endswith('.ttc'):
                    pdfmetrics.registerFont(TTFont('NotoSansSC', font_path, subfontIndex=0))
                else:
                    pdfmetrics.registerFont(TTFont('NotoSansSC', font_path))
                FONT_NAME_BODY = "NotoSansSC"
                FONT_NAME_ENG = "NotoSansSC"
                break
        except Exception:
            continue
    
    # 尝试加载Noto Sans KR-Medium（韩语）
    kr_fonts = [
        os.path.join(font_dir, 'NotoSansKR-Medium.ttf'),  # 项目字体文件夹
        "C:\\Windows\\Fonts\\NotoSansKR-Medium.ttf",      # 系统字体
        "C:\\Windows\\Fonts\\NotoSansKR-VF.ttf",           # 系统可变字体
    ]
    
    for font_path in kr_fonts:
        try:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('NotoSansKR-Medium', font_path))
                FONT_NAME_KR = "NotoSansKR-Medium"
                break
        except Exception:
            continue
    
    # 如果都失败了，使用Helvetica
    if FONT_NAME_BODY == "Helvetica":
        FONT_NAME_BODY = "Helvetica"
        FONT_NAME_ENG = "Helvetica"
        FONT_NAME_KR = "Helvetica"

def detect_font_for_text(text):
    """检测文本中包含的字符类型，返回合适的字体名称
    
    Args:
        text: 要检测的文本
        
    Returns:
        str: 字体名称
    """
    # 检查是否包含韩文字符 (Unicode范围: AC00-D7AF)
    has_korean = any('\uAC00' <= char <= '\uD7AF' for char in text)
    
    if has_korean:
        return FONT_NAME_KR
    else:
        return FONT_NAME_BODY

try:
    from pypdf import PdfWriter as PdfMerger 
except ImportError:
    PdfMerger = None

from function.file_utils import find_files_recursively, get_organized_path, get_save_path
from function.parsers import parse_subtitle_to_list
from function.naming import generate_output_name, clean_filename_title
from function.volumes import smart_group_files

class Bookmark(Flowable):
    """PDF书签生成器
    
    用于在PDF文档中创建书签，方便导航。
    """
    def __init__(self, key): 
        """初始化书签
        
        Args:
            key: 书签标识符
        """
        Flowable.__init__(self)
        self.key = key
    
    def draw(self): 
        """绘制书签"""
        self.canv.bookmarkPage(self.key)
    
    def wrap(self, w, h): 
        """设置书签大小
        
        Args:
            w: 宽度
            h: 高度
            
        Returns:
            tuple: 书签大小 (0, 0)
        """
        return (0, 0)

class OutlineEntry(Flowable):
    """PDF大纲条目生成器
    
    用于在PDF文档中创建大纲条目，方便导航。
    """
    def __init__(self, t, k): 
        """初始化大纲条目
        
        Args:
            t: 大纲标题
            k: 关联的书签标识符
        """
        Flowable.__init__(self)
        self.title = t
        self.key = k
    
    def draw(self): 
        """绘制大纲条目"""
        self.canv.addOutlineEntry(self.title, self.key, level=0, closed=True)
    
    def wrap(self, w, h): 
        """设置大纲条目大小
        
        Args:
            w: 宽度
            h: 高度
            
        Returns:
            tuple: 大纲条目大小 (0, 0)
        """
        return (0, 0)

class TOCFinished(Flowable):
    """目录结束标记
    
    用于标记PDF目录生成结束。
    """
    def wrap(self, w, h): 
        """设置目录结束标记大小
        
        Args:
            w: 宽度
            h: 高度
            
        Returns:
            tuple: 标记大小 (0, 0)
        """
        return (0, 0)
    
    def draw(self): 
        """绘制目录结束标记"""
        pass

class SetHeaderTitle(Flowable):
    """设置PDF页眉标题
    
    用于设置PDF文档的页眉标题。
    """
    def __init__(self, title):
        """初始化页眉标题设置
        
        Args:
            title: 页眉标题
        """
        Flowable.__init__(self)
        self.title = title
    
    def wrap(self, w, h): 
        """设置页眉标题大小
        
        Args:
            w: 宽度
            h: 高度
            
        Returns:
            tuple: 标题大小 (0, 0)
        """
        return (0, 0)
    
    def draw(self):
        """绘制页眉标题设置"""
        if hasattr(self.canv, '_doctemplate'):
            self.canv._doctemplate.current_header_title = self.title

class MyDocTemplate(SimpleDocTemplate):
    """自定义PDF文档模板
    
    扩展SimpleDocTemplate，添加自定义页眉和目录生成功能。
    """
    def __init__(self, filename, **kw):
        """初始化自定义文档模板
        
        Args:
            filename: 输出文件名
            **kw: 其他参数
        """
        SimpleDocTemplate.__init__(self, filename, **kw)
        self.current_header_title = ""
    
    def afterFlowable(self, flowable):
        """处理流对象后的事件
        
        Args:
            flowable: 流对象
        """
        if isinstance(flowable, Paragraph) and flowable.style.name == 'ChapterTitle':
            key = getattr(flowable, '_bookmarkName', None)
            if key: 
                self.notify('TOCEntry', (0, flowable.getPlainText(), self.page, key))
    
    def handle_pageBegin(self):
        """处理页面开始事件"""
        super().handle_pageBegin()
        self._draw_custom_header()
    
    def _draw_custom_header(self):
        """绘制自定义页眉"""
        if not self.current_header_title: 
            return
        
        c = self.canv
        c.saveState()
        # 根据页眉标题内容动态选择字体
        header_font = detect_font_for_text(self.current_header_title)
        # 使用已加载的字体
        try:
            c.setFont(header_font, 9)
        except Exception as e:
            print(f"设置字体失败，使用默认字体: {e}")
            c.setFont('Helvetica', 9)
        c.setFillColor(colors.gray)
        page_width, page_height = self.pagesize
        c.drawCentredString(page_width / 2.0, page_height - 15 * mm, self.current_header_title)
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(0.5)
        c.line(20*mm, page_height - 18*mm, page_width - 20*mm, page_height - 18*mm)
        c.restoreState()

def run_pdf_task(target_dir, log_func, progress_bar, root, batch_size=0, output_dir=None, volume_pattern="智能", stop_flag=[False]):
    """运行PDF文档生成任务
    
    从指定目录扫描字幕文件，生成带时间戳和目录的PDF文档。
    
    Args:
        target_dir: 目标目录
        log_func: 日志记录函数
        progress_bar: 进度条信号
        root: 根窗口
        batch_size: 批量大小
        output_dir: 输出目录
        volume_pattern: 分卷模式
    """
    # 初始化字体
    init_fonts()
    log_func(f"[PDF生成] 扫描目录: {target_dir.replace('/', '\\')}", tag="pdf_red")
    # 递归查找字幕文件
    files = find_files_recursively(target_dir, ('.srt', '.vtt', '.ass'))
    if not files: 
        return log_func("❌ 未找到字幕文件。")

    # 智能分组文件
    file_groups = smart_group_files(files, batch_size)
    total_files = len(files)
    processed_count = 0

    # 设置PDF样式
    styles = getSampleStyleSheet()
    
    # 使用已加载的字体
    h1 = ParagraphStyle('ChapterTitle', 
                       fontName=FONT_NAME_BODY, 
                       fontSize=16, 
                       leading=20, 
                       spaceAfter=10, 
                       textColor=colors.darkblue)
    toc_h = ParagraphStyle('TOCHeader', 
                          fontName=FONT_NAME_BODY, 
                          fontSize=20, 
                          alignment=TA_CENTER)
    body = ParagraphStyle('SubtitleBody', 
                         fontName=FONT_NAME_BODY, 
                         fontSize=10, 
                         leading=14, 
                         spaceAfter=4, 
                         alignment=TA_LEFT)
    
    # 为目录项设置样式，支持韩语
    toc_text = ParagraphStyle('TOCText', 
                             fontName=FONT_NAME_BODY, 
                             fontSize=12)
    toc_link = ParagraphStyle('TOCLink', 
                             parent=toc_text, 
                             textColor=colors.blue)
    
    # 更新样式表
    styles.add(toc_text)
    styles.add(toc_link)

    # 确定基础输出目录
    base_output_dir = output_dir if output_dir else target_dir

    for group in file_groups:
        # 检查停止标志
        if stop_flag[0]:
            return
            
        if not group: 
            continue
        
        # 生成输出文件名
        out_name = generate_output_name([os.path.basename(f) for f in group], ".pdf", volume_pattern)
        # 获取组织化路径
        out_path = get_organized_path(base_output_dir, out_name)
        
        try:
            # 生成PDF文档
            doc = MyDocTemplate(out_path, pagesize=A4, topMargin=25*mm, bottomMargin=25*mm, leftMargin=25*mm, rightMargin=25*mm)
            frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
            doc.addPageTemplates([PageTemplate(id='normal', frames=frame)])
            # 创建目录对象并配置样式
            toc = TableOfContents()
            toc.levelStyles = [
                ParagraphStyle('TOCLevel1', 
                             fontName=FONT_NAME_KR, 
                             fontSize=12, 
                             leftIndent=20, 
                             firstLineIndent=-20, 
                             spaceBefore=5),
                ParagraphStyle('TOCLevel2', 
                             fontName=FONT_NAME_KR, 
                             fontSize=11, 
                             leftIndent=40, 
                             firstLineIndent=-20, 
                             spaceBefore=3)
            ]
            story = [Bookmark("TOC"), OutlineEntry("Content", "TOC"), Paragraph("Content", toc_h), toc, TOCFinished(), PageBreak()]
            
            for i, fp in enumerate(group):
                # 检查停止标志
                if stop_flag[0]:
                    log_func("⚠️ 任务已被用户停止")
                    return
                    
                clean_title = clean_filename_title(os.path.basename(fp))
                story.append(SetHeaderTitle(clean_title))
                if i > 0: 
                    story.append(PageBreak())
                    
                # 根据标题内容动态选择字体
                title_font = detect_font_for_text(clean_title)
                # 创建动态标题样式
                dynamic_h1 = ParagraphStyle('ChapterTitle', 
                                           fontName=title_font, 
                                           fontSize=16, 
                                           leading=20, 
                                           spaceAfter=10, 
                                           textColor=colors.darkblue)
                p = Paragraph(clean_title, dynamic_h1)
                p._bookmarkName = f"CH_{processed_count}"
                story.extend([Bookmark(p._bookmarkName), OutlineEntry(clean_title, p._bookmarkName), p, Spacer(1, 10)])
                
                # 解析字幕内容
                content_list = parse_subtitle_to_list(fp)
                if not content_list:
                    story.append(Paragraph("<i>[无对白]</i>", body))
                else:
                    for time_str, text in content_list:
                        # 检查停止标志
                        if stop_flag[0]:
                            log_func("⚠️ 任务已被用户停止")
                            return
                            
                        safe_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        # 根据文本内容选择合适的字体
                        font_name = detect_font_for_text(text)
                        # 创建动态字体样式
                        dynamic_body = ParagraphStyle('DynamicBody', 
                                                    fontName=font_name, 
                                                    fontSize=10, 
                                                    leading=14, 
                                                    spaceAfter=4, 
                                                    alignment=TA_LEFT)
                        story.append(Paragraph(f"<b>[{time_str}]</b>  {safe_text}", dynamic_body))
                
                processed_count += 1
                # 更新进度，支持不同类型的进度回调
                try:
                    # 尝试PyQt的信号方式（progress_bar是信号对象）
                    progress_bar.emit(int(processed_count / total_files * 100))
                except AttributeError:
                    try:
                        # 尝试直接调用方式（progress_bar是emit方法本身）
                        progress_bar(int(processed_count / total_files * 100))
                    except Exception as e:
                        pass
            
            # 生成PDF
            doc.multiBuild(story)
            log_func(f"📄 已生成: {os.path.join('pdf', out_name).replace('/', '\\')}", tag="pdf_red")
        except Exception as e: 
            log_func(f"❌ 失败: {e}")
    
    # 重置进度条
    try:
        progress_bar.emit(0)
    except AttributeError:
        try:
            progress_bar(0)
        except Exception as e:
            pass

