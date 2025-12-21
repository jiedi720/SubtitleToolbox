🎬 Subtitle Toolbox (字幕工具箱)
Subtitle Toolbox 是一个功能强大的本地化字幕处理工具，专为剧集爱好者和语言学习者设计。它可以批量处理 SRT/VTT/ASS 字幕，将其转换为便于阅读的 PDF、Word 或 TXT 剧本，并支持智能合并与格式清洗。

✨ 核心功能 (Features)
1. 📖 多格式剧本生成 (Script Generation)
不再受限于播放器，将字幕转换为可打印、可编辑的文档：

SRT 转 PDF: 生成排版精美的 PDF 剧本。

✅ 智能排版: 严格保持逐行显示，支持目录（TOC）和书签跳转。

✅ 字体防乱码: 自动调用系统 Malgun Gothic (韩文) 和 微软雅黑，完美支持中韩双语。

✅ 时间轴: 保留关键时间轴 [00:00:06]，重点加粗显示。

SRT 转 Word: 使用 python-docx 快速生成 .docx 文档，方便后续编辑。

SRT 转 TXT: 生成纯文本剧本，支持保留时间轴或仅保留纯对白。

2. 🔄 智能文件合并 (Smart Merging)
支持将分集的剧本合并为一整季的“全剧本”：

Word 合并: 调用原生 MS Word (Win32 COM) 接口，完美保留源文档的格式、页眉页脚和排版。

PDF 合并: 快速合并多个 PDF 文件。

TXT 合并: 将多个文本文件汇总，自动添加分集标题分隔符。

3. 🛠️ ASS 字幕样式批处理
样式重置: 一键统一修改 ASS 字幕的字体、大小、边框阴影。

双语分离: 针对中韩/中英双语字幕，可独立配置中文和外语的样式（如中文宋体、韩文衬线体）。

4. ⚡ 实用特性
智能编码识别: 自动检测 UTF-8, GBK, EUC-KR, UTF-16，彻底告别乱码。

文件名清洗: 自动去除文件名中的 1080p, Netflix, WEB-DL 等冗余标签，生成干净的标题。

模块化架构: 逻辑分离，稳定高效。

🚀 安装与运行 (Installation)
1. 环境要求
Windows 10/11 (因为使用了 Win32 COM 调用 Word)

Python 3.8+

Microsoft Word (用于 Word 合并功能)

2. 安装依赖库
请在项目根目录下运行：

Bash

pip install -r requirements.txt
(如果没有 requirements.txt，请安装以下库)：

Bash

pip install pysrt reportlab python-docx pywin32 pypdf
3. 运行程序

📦 打包为 EXE (Building)
如果你想将程序打包为独立的 .exe 文件分享给他人，请使用 PyInstaller。

完整打包命令 (v1.0):

PowerShell
python -m PyInstaller --onefile --windowed --name="SubtitleToolbox" --icon="subtitle-toolbox.ico" --add-data "logic;logic" --add-data "subtitle-toolbox.ico;." --hidden-import="reportlab" --hidden-import="reportlab.platypus" --hidden-import="reportlab.lib.styles" --hidden-import="reportlab.platypus.tableofcontents" --hidden-import="win32timezone" --hidden-import="pysrt" --hidden-import="docx" --hidden-import="docxcompose" --hidden-import="win32com" --hidden-import="win32com.client" --hidden-import="pythoncom" --hidden-import="pypdf" --hidden-import="utils" --hidden-import="config" --clean main.py

优化: 文件扫描支持包含 [] 等特殊字符的路径。

🤝 贡献与同步 (Contributing)
本项目包含一个一键同步脚本 update.bat。 如果你修改了本地代码，双击该脚本即可自动提交并强制推送到 GitHub 仓库。# -
