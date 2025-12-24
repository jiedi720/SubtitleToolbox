# SubtitleToolbox

**SubtitleToolbox** 是一款专为字幕组及翻译从业者设计的现代化、全功能自动化工具箱。它通过多线程异步架构，将复杂的剧本处理、字幕转换及临时文件维护工作流整合进一个直观的 GUI 界面中。

---

## 📂 项目目录结构 (A-Z 排序)

```text
SubtitleToolbox/
├── SubtitleToolbox.py         # 程序唯一入口
├── SubtitleToolbox.ini        # 运行配置持久化文件 (自动生成)
├── build_exe.bat              # PyInstaller 一键打包脚本
│
├── config/                    # 配置
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
│   ├── font.py                # 字体库匹配与路径处理
│   └── srt2ass.py             # 样式转换扩展增强
│
├── function/                  # 功能层 (Function)
│   ├── cleaners.py            # 文本清洗与冗余剔除工具
│   ├── files.py               # 文件扫描与读写封装
│   ├── naming.py              # 自动化命名规则匹配
│   ├── parsers.py             # 内容解析器
│   ├── paths.py               # 增强型路径/目录格式化
│   └── trash.py               # 回收站智能清理 (带文件占用追踪)
│
├── gui/                       # 界面层 (View)
│   ├── ass_gui.py             # ASS 样式可视化配置弹窗
│   ├── components_gui.py      # 复用型 UI 组件封装
│   ├── log_gui.py             # 交互式多色控制台组件
│   └── main_gui.py            # 主面板布局与组件集成
│
├── logic/                     # 业务逻辑层 (Logic)
│   ├── pdf_logic.py           # PDF 页面缝合与重组
│   ├── srt2ass_logic.py       # SRT 到 ASS 字幕转换核心实现
│   ├── txt_logic.py           # TXT 极速合并算法
│   └── word_logic.py          # Word (win32com) 文档驱动逻辑
│
└── resources/                 # 外部资源
    └── SubtitleToolbox.ico    # 程序封装图标

```

---

## 🚀 核心功能特性

* **安全清理 (Cleanup Tool)**：使用 `send2trash` 安全移除临时文件，支持文件锁定（占用）自动识别与报红提示。
* **交互控制台 (Interactive Log)**：自适应主题的多色日志系统，精准反馈任务状态（✅成功 / 🔴错误 / 🔵提示）。
* **剧本自动化 (SCRIPT 模式)**：支持 TXT、Word、PDF 一键合并，内置 `Smart Grouping` 逻辑实现自动分卷。
* **异步架构 (Async Engine)**：所有核心任务跑在独立线程，确保处理超大剧本时 GUI 永不卡死。
* **样式定制 (SRT2ASS 模式)**：可视化调整字幕字体、色值及阴影，配置即时保存至 `.ini` 文件。

---

## 📦 依赖库清单 (requirements.txt / A-Z 排序)

```text
customtkinter      # 现代化 UI 框架
docxcompose        # Word 深度合并
pypdf              # PDF 合并与处理
pysrt              # SRT 字幕解析
pysubs2            # ASS 字幕处理
python-docx        # Word 文档解析
pywin32            # Windows COM 组件调用 (Word 驱动)
reportlab          # PDF 生成与绘图支持
send2trash         # 安全回收站操作

```

---

## 🛠️ 打包指南

项目已针对 PyInstaller 优化，运行 `build_exe.bat` 即可。

**关键参数说明：**

* `--add-data`：采用递归封装，确保所有子模块打入 EXE。
* `--collect-all "send2trash"`：解决回收站 DLL 组件丢失问题。
* `--windowed`：消除启动时的控制台黑窗。