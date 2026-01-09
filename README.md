# SubtitleToolbox

**SubtitleToolbox** 是一款专为字幕组及翻译从业者设计的现代化、全功能自动化工具箱。它通过多线程异步架构，将复杂的剧本处理、字幕转换、文档合并、语音识别及临时文件维护工作流整合进一个直观的 GUI 界面中。

---

## 📂 项目目录结构

```text
SubtitleToolbox/
├── SubtitleToolbox.py         # 程序唯一入口
├── SubtitleToolbox.ini        # 运行配置持久化文件 (自动生成)
├── SubtitleToolbox.exe        # 打包后的可执行文件
├── build_exe.bat              # PyInstaller 一键打包脚本
├── SubtitleToolbox.spec       # PyInstaller 打包配置文件
│
├── function/                  # 功能层 (Function)
│   ├── __init__.py            # 功能模块统一导入接口
│   ├── AutoSubtitles.py       # AutoSub 语音识别核心模块
│   ├── controllers.py         # 主控制器，协调 GUI 和任务执行
│   ├── file_utils.py          # 文件扫描与读写封装
│   ├── merge.py               # PDF/TXT/Word 文档合并功能
│   ├── naming.py              # 自动化命名规则匹配
│   ├── parsers.py             # 字幕内容解析器
│   ├── settings.py            # 配置读写与管理逻辑
│   ├── tasks.py               # 任务执行调度模块
│   ├── trash.py               # 回收站智能清理
│   └── volumes.py             # 分卷逻辑处理模块
│
├── font/                      # 字体与格式增强
│   ├── __init__.py            # 字体模块统一导入接口
│   ├── NotoSansKR-Medium.ttf  # 韩语字体文件
│   └── srt2ass.py             # SRT 转 ASS 字幕转换模块
│
├── gui/                       # 界面层 (View)
│   ├── __init__.py            # GUI 模块统一导入接口
│   ├── log_gui.py             # 交互式多色控制台组件
│   ├── qt_gui.py              # 主面板布局与组件集成
│   ├── theme.py               # 主题切换模块
│   └── ui_SubtitleToolbox.py  # UI 界面定义文件
│
├── logic/                     # 业务逻辑层 (Logic)
│   ├── __init__.py            # 逻辑模块统一导入接口
│   ├── pdf_logic.py           # PDF 文档生成与合并
│   ├── txt_logic.py           # TXT 文档生成
│   └── word_logic.py          # Word 文档生成
│
├── icons/                     # 图标资源
│   ├── PDF.png                # PDF 文件图标
│   ├── SubtitleToolbox.ico    # 程序封装图标
│   ├── Word.ico               # Word 文件图标
│   └── ...                    # 其他功能图标
│
└── venv/                      # Python 虚拟环境
```

---

## 🚀 核心功能特性

### 四大核心模式

#### 1. Script 模式 (剧本自动化)
- 支持从字幕文件生成 TXT、Word、PDF 三种格式文档
- 内置智能分组逻辑，支持整季、智能、单集三种分卷模式
- 自动解析字幕时间轴，生成带时间戳的文档
- 支持中韩英等多语言字幕处理
- 自动分类输出文件到对应目录（pdf/、word/、txt/）

#### 2. Srt2Ass 模式 (字幕转换)
- 自动匹配双语字幕文件（中韩配对）
- 将 SRT 字幕转换为 ASS 格式
- 支持自定义字幕样式（字体、颜色、大小等）
- 自动归档原始 SRT 文件到 srt/ 目录
- 支持多种编码的字幕文件读取

#### 3. Merge 模式 (文档合并)
- 支持合并多个 PDF 文件
- 支持合并多个 TXT 文件
- 支持合并多个 Word 文档（保留页眉页脚和格式）
- 智能识别文件类型，自动分类处理

#### 4. AutoSub 模式 (语音识别) 
- 基于 faster-whisper 的语音识别功能
- 支持音频文件（.mp3）和视频文件（.mp4、.mkv、.avi）
- 自动检测语言或指定语言（韩语、日语、英语、中文）
- GPU/CPU 自动切换，确保最佳性能
- 批量处理，支持跳过已有字幕的文件
- 实时进度显示和日志输出

### 其他核心功能

- **安全清理 (Cleanup Tool)**：使用 `send2trash` 安全移除临时文件，支持文件锁定（占用）自动识别与报红提示，永不删除 .srt 原始文件
- **交互控制台 (Interactive Log)**：自适应主题的多色日志系统，精准反馈任务状态（✅成功 / 🔴错误 / 🔵Word / 📄PDF）
- **异步架构 (Async Engine)**：所有核心任务跑在独立线程，确保处理超大剧本时 GUI 永不卡死
- **主题切换**：支持浅色/深色/系统三种主题模式，实时切换，主题设置自动保存
- **配置管理**：所有设置自动保存至 `.ini` 文件，支持多预设管理
- **智能路径处理**：自动分类输出文件到对应目录（pdf/、word/、txt/、srt/）
- **固定图标颜色**：按钮图标颜色固定为黑色，不随主题变化，确保视觉一致性

---

## 📦 依赖库清单

```text
# GUI 框架
PySide6>=6.10.0
shiboken6>=6.10.0

# 字幕处理
pysrt>=1.1.0
pysubs2>=1.7.0

# 文档生成
python-docx>=1.0.0
reportlab>=4.0.0
pypdf>=3.0.0

# 文件处理
send2trash>=1.8.0

# 语音识别
faster-whisper>=1.0.0
ctranslate2>=4.0.0

# GPU 支持（可选）
nvidia-cuda-runtime-cu12>=12.0
nvidia-cudnn-cu12>=9.0

# 其他依赖
huggingface-hub>=0.20.0
tokenizers>=0.15.0
numpy>=1.0.0
```

**安装方法：**

```bash
pip install -r requirements.txt
```

---

## 🛠️ 打包指南

项目已针对 PyInstaller 优化，提供打包脚本：

- `build_exe.bat` - PyInstaller 一键打包脚本
- `SubtitleToolbox.spec` - PyInstaller 打包配置文件

**关键参数说明：**

- `--onefile`：打包成单个 EXE 文件
- `--windowed`：消除启动时的控制台黑窗
- `--icon`：设置程序图标为 `icons/SubtitleToolbox.ico`
- `--optimize=2`：最高级别的字节码优化
- `--upx=True`：启用 UPX 压缩减小体积
- 排除不必要的模块（tkinter、PyQt5/6、pandas 等）

**使用方法：**

直接运行 `build_exe.bat` 即可生成 `SubtitleToolbox.exe`。

---

## 🎨 使用说明

### Script 模式
1. 选择源目录：点击"浏览"按钮选择包含字幕文件的目录
2. 选择输出目录（可选）：自定义输出位置，默认为源目录
3. 选择输出格式：勾选需要生成的文档格式（TXT/Word/PDF）
4. 选择分卷模式：整季/智能/单集
5. 点击"开始"按钮执行任务

### Srt2Ass 模式
1. 选择源目录：点击"浏览"按钮选择包含 SRT 字幕的目录
2. 选择输出目录（可选）：自定义输出位置
3. 点击"开始"按钮执行转换

### Merge 模式
1. 选择源目录：点击"浏览"按钮选择需要合并的文件目录
2. 选择输出目录：自定义合并后的文件输出位置
3. 点击"开始"按钮执行合并

### AutoSub 模式 🆕
1. 选择源目录：点击"浏览"按钮选择音频或视频文件目录
2. 选择语言模式：
   - 自动：让 Whisper 自动检测语言
   - 指定语言：韩语/日语/英语/中文
3. 选择模型：使用本地模型或在线下载
4. 点击"开始"按钮执行语音识别
5. 查看日志：实时查看处理进度和结果

---

## 📝 技术架构

项目采用 **MVC 架构** 设计：

- **Model (logic/ + function/)**：业务逻辑层，负责文档生成、字幕解析、文件处理、语音识别等核心功能
- **View (gui/)**：视图层，负责用户界面展示和交互
- **Controller (function/controllers.py)**：控制层，负责协调各模块、管理状态和配置

**多线程设计**：所有耗时任务均在独立线程中执行，通过信号槽机制与 UI 通信，确保界面响应流畅。

**模块化设计**：每个功能模块独立封装，便于维护和扩展。

**UI 设计**：使用 Qt Designer 设计界面，通过 PySide6 实现，支持主题切换和自定义样式。

---

## 🔧 系统要求

- **操作系统**：Windows 10/11（推荐）
- **Python**：3.8 或更高版本
- **GPU**（可选）：NVIDIA GPU（推荐，用于加速语音识别）
- **内存**：建议 8GB 或以上
- **存储空间**：至少 500MB 可用空间

---

## 📄 许可证

本项目仅供学习和个人使用。