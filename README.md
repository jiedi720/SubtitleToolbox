# 🎬 Subtitle Toolbox (字幕工具箱) v2.1

**Subtitle Toolbox** 是一款专为剧本制作和字幕处理设计的本地工具。它能将 SRT/ASS/VTT 批量转换为排版精美的 PDF、Word 或 TXT 剧本，并支持高级 ASS 样式自定义。

> **v2.1 更新亮点**：模块化架构重构、智能页眉支持、以及“根目录优先”的零污染合并逻辑。

---

## ✨ 核心功能

### 1. 剧本生成与格式化

* **📄 PDF 剧本**: 自动生成目录，支持**居中页眉**（动态显示当前集数），每一页均有清晰的标注。
* **📝 Word 文档**: 使用分节符技术，确保每集拥有独立页眉，文字居中排版。
* **🎨 ASS 转换**: 强大的内置样式编辑器，支持韩/中、英/中等多语种字幕样式批量转换。

### 2. 智能合并逻辑 (v2.1 新特性)

合并功能采用 **“非贪婪优先级”** 策略，旨在保持工作目录简洁：

* **优先级 1 (根目录)**: 优先扫描选定目录下的文件。若发现目标格式，立即执行合并。
* **优先级 2 (子目录)**: 仅当根目录无文件时，才会自动进入 `pdf/`, `word/` 或 `txt/` 子文件夹进行合并。
* **零污染**: 合并任务不再自动创建 `script` 文件夹，确保“原地操作”或“精准操作”。

### 3. 处理与安全

* **🔍 深度扫描**: 支持递归扫描，自动识别所有子文件夹中的字幕源文件。
* **📦 自动归档**: 生成任务会将文件分类存放在 `script/` 下的对应子目录中。
* **🗑️ 安全清理**: 清空输出目录时调用系统回收站 (`send2trash`)，而非永久删除。
* **⚙️ 路径确认**: 增加 `👉` 确认按钮，支持手动触发路径验证与状态更新。

---

## 🛠️ 模块化项目结构

项目采用界面与逻辑分离的架构，极大提升了扩展性：

```text
subtitle_toolbox/
├── main.py              # 程序入口：负责线程调度与核心变量管理
├── gui.py               # 界面模块：负责所有 Tkinter 布局与 UI 交互
├── logic/               # 逻辑内核
│   ├── pdf_logic.py     # PDF 动态页眉生成与优先级合并
│   ├── word_logic.py    # Word 分节处理与 Win32 合并引擎
│   ├── txt_logic.py     # 纯文本提取与编码兼容处理
│   ├── ass_logic.py     # 字幕样式转换引擎
│   └── utils.py         # 万能解析器 (UTF-8/16/GBK) 与通用工具
└── resources/           # 静态资源 (图标、字体等)

```

---

## 📦 快速开始

### 安装依赖

```bash
pip install reportlab python-docx pysrt pywin32 send2trash pypdf

```

### 打包命令 (PyInstaller)

使用以下命令可将项目打包为独立的 EXE 文件，已包含所有隐藏导入：

```bash
python -m PyInstaller --noconfirm --onefile --windowed \
--name="SubtitleToolbox" \
--icon="resources/subtitle-toolbox.ico" \
--add-data "logic;logic" \
--add-data "resources;resources" \
--hidden-import="reportlab" \
--hidden-import="reportlab.platypus" \
--hidden-import="reportlab.lib.styles" \
--hidden-import="pysrt" \
--hidden-import="docx" \
--hidden-import="win32com" \
--hidden-import="pypdf" \
--hidden-import="send2trash" \
--clean main.py

```

---

## 📝 使用指南

1. **生成剧本**：
* 选择源目录，勾选任务模式为“生成台词剧本”。
* 程序会在 `script/` 下创建对应的格式文件夹并分类存放。


2. **合并剧本**：
* 若想合并 `script/pdf` 里的文件，直接点击“PDF合并”即可。
* 若想合并根目录下的文件，只需确保根目录下有 PDF，点击合并时程序会优先处理根目录，**不会**生成多余文件夹。


3. **快捷键**：在路径框按下 `Enter` 或点击 `👉` 即可快速验证路径有效性。

---

## 📄 开源协议

本项目遵循 MIT License 协议。