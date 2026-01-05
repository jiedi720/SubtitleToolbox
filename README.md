# SubtitleToolbox

**SubtitleToolbox** 是一款专为字幕组及翻译从业者设计的现代化、全功能自动化工具箱。它通过多线程异步架构，将复杂的剧本处理、字幕转换、文档合并及临时文件维护工作流整合进一个直观的 GUI 界面中。

---

## 📂 项目目录结构 (A-Z 排序)

```text
SubtitleToolbox/
├── SubtitleToolbox.py         # 程序唯一入口
├── SubtitleToolbox.ini        # 运行配置持久化文件 (自动生成)
├── SubtitleToolbox.exe        # 打包后的可执行文件
├── build_exe.bat              # PyInstaller 一键打包脚本
├── updateGithub.bat           # GitHub 更新脚本
├── updateGithub.ps1           # GitHub 更新 PowerShell 脚本
│
├── config/                    # 配置
│   ├── __init__.py            # 配置模块统一导入接口
│   └── settings.py            # 配置读写与管理逻辑
│
├── control/                   # 控制层 (Controller)
│   ├── base_controller.py     # 路径管理与通用基础逻辑
│   ├── main_controller.py     # 全局模式切换调度
│   ├── task_controller.py     # 核心任务流程控制
│   ├── tool_controller.py     # 外部工具 (合并/清理) 调用中枢
│   └── ui_controller.py       # UI 交互状态调度
│
├── font/                      # 字体与格式增强
│   ├── __init__.py            # 字体模块统一导入接口
│   ├── NotoSansKR-Medium.ttf  # 韩语字体文件
│   └── srt2ass.py             # SRT转ASS字幕转换模块
│
├── function/                  # 功能层 (Function)
│   ├── __init__.py            # 功能模块统一导入接口
│   ├── cleaners.py            # 文本清洗与冗余剔除工具
│   ├── files.py               # 文件扫描与读写封装
│   ├── merge.py               # PDF/TXT/Word文档合并功能
│   ├── naming.py              # 自动化命名规则匹配
│   ├── parsers.py             # 字幕内容解析器
│   ├── paths.py               # 增强型路径/目录格式化
│   ├── trash.py               # 回收站智能清理 (带文件占用追踪)
│   └── volumes.py             # 分卷逻辑处理模块
│
├── gui/                       # 界面层 (View)
│   ├── Icons.qrc              # 图标资源文件
│   ├── Icons_rc.py            # 图标资源编译文件
│   ├── __init__.py            # GUI模块统一导入接口
│   ├── log_gui.py             # 交互式多色控制台组件
│   ├── qt_gui.py              # 主面板布局与组件集成
│   ├── theme.py               # 主题切换模块
│   └── ui_SubtitleToolbox.py  # UI界面定义文件
│
├── logic/                     # 业务逻辑层 (Logic)
│   ├── __init__.py            # 逻辑模块统一导入接口
│   ├── pdf_logic.py           # PDF文档生成与合并
│   ├── txt_logic.py           # TXT文档生成
│   └── word_logic.py          # Word文档生成
│
└── resources/                 # 外部资源
    ├── PDF.ico                # PDF文件图标
    ├── SubtitleToolbox.ico    # 程序封装图标
    ├── Word.ico               # Word文件图标
    ├── checkmark.png          # 勾选标记图标
    ├── txt.ico                # TXT文件图标
    └── SubtitleToolbox.ui     # Qt Designer UI设计文件

```

---

## 🚀 核心功能特性

### 三大核心模式

* **Script 模式 (剧本自动化)**：
  - 支持从字幕文件生成 TXT、Word、PDF 三种格式文档
  - 内置智能分组逻辑，支持整季、智能、单集三种分卷模式
  - 自动解析字幕时间轴，生成带时间戳的文档
  - 支持中韩英等多语言字幕处理
  - 自动分类输出文件到对应目录（pdf/、word/、txt/、srt/）

* **Srt2Ass 模式 (字幕转换)**：
  - 自动匹配双语字幕文件（中韩配对）
  - 将 SRT 字幕转换为 ASS 格式
  - 支持自定义字幕样式（字体、颜色、大小等）
  - 自动归档原始 SRT 文件到 srt/ 目录
  - 支持多种编码的字幕文件读取

* **Merge 模式 (文档合并)**：
  - 支持合并多个 PDF 文件
  - 支持合并多个 TXT 文件
  - 支持合并多个 Word 文档（保留页眉页脚和格式）
  - 智能识别文件类型，自动分类处理

### 其他核心功能

* **安全清理 (Cleanup Tool)**：使用 `send2trash` 安全移除临时文件，支持文件锁定（占用）自动识别与报红提示，永不删除 .srt 原始文件。
* **交互控制台 (Interactive Log)**：自适应主题的多色日志系统，精准反馈任务状态（✅成功 / 🔴错误 / 🔵Word / 📄PDF）。
* **异步架构 (Async Engine)**：所有核心任务跑在独立线程，确保处理超大剧本时 GUI 永不卡死。
* **主题切换**：支持浅色/深色/系统三种主题模式，实时切换，主题设置自动保存。
* **配置管理**：所有设置自动保存至 `.ini` 文件，支持多预设管理。
* **智能路径处理**：自动分类输出文件到对应目录（pdf/、word/、txt/、srt/）。
* **固定图标颜色**：按钮图标颜色固定为黑色，不随主题变化，确保视觉一致性。

---

## 📦 依赖库清单

```text
PySide6>=6.0.0      # GUI 框架
pysrt>=1.1.0         # SRT 字幕处理
pysubs2>=1.7.0       # 通用字幕格式处理
python-docx>=1.0.0   # Word 文档生成
reportlab>=4.0.0     # PDF 文档生成
pypdf>=3.0.0         # PDF 文档处理
send2trash>=1.8.0    # 文件删除到回收站
```

**安装方法：**

```bash
pip install -r requirements.txt
```

或直接运行：

```bash
pip install ^
    PySide6>=6.0.0 ^      # GUI 框架
    pysrt>=1.1.0 ^         # SRT 字幕处理
    pysubs2>=1.7.0 ^       # 通用字幕格式处理
    python-docx>=1.0.0 ^   # Word 文档生成
    reportlab>=4.0.0 ^     # PDF 文档生成
    pypdf>=3.0.0 ^         # PDF 文档处理
    send2trash>=1.8.0 ^    # 文件删除到回收站
```

---

## 🛠️ 打包指南

项目已针对 PyInstaller 优化，提供打包脚本：

* `build_exe.bat` - PyInstaller 一键打包脚本

**关键参数说明：**

* `--onefile`：打包成单个 EXE 文件
* `--windowed`：消除启动时的控制台黑窗
* `--icon`：设置程序图标为 `resources/SubtitleToolbox.ico`
* `--optimize=2`：最高级别的字节码优化
* `--upx=True`：启用 UPX 压缩减小体积
* 排除不必要的模块（tkinter、PyQt5/6、numpy、pandas 等）

**使用方法：**

直接运行 `build_exe.bat` 即可生成 `SubtitleToolbox.exe`。

---

## 🎨 使用说明

1. **选择源目录**：点击"浏览"按钮选择包含字幕文件的目录
2. **选择输出目录**（可选）：自定义输出位置，默认为源目录
3. **选择功能模式**：在三个标签页中选择 Script / Srt2Ass / Merge
4. **配置选项**：根据需要勾选输出格式或合并选项
5. **开始处理**：点击"开始"按钮执行任务
6. **查看日志**：在日志区域查看任务进度和结果
7. **清理文件**：使用"清理"按钮安全删除生成的临时文件

---

## 📝 技术架构

项目采用 **MVC 架构** 设计：

* **Model (logic/ + function/)**：业务逻辑层，负责文档生成、字幕解析、文件处理等核心功能
* **View (gui/)**：视图层，负责用户界面展示和交互
* **Controller (control/)**：控制层，负责协调各模块、管理状态和配置

**多线程设计**：所有耗时任务均在独立线程中执行，通过信号槽机制与 UI 通信，确保界面响应流畅。

**模块化设计**：每个功能模块独立封装，便于维护和扩展。

**UI 设计**：使用 Qt Designer 设计界面，通过 PySide6 实现，支持主题切换和自定义样式。