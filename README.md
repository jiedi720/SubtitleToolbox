# 📖 Subtitle Toolbox (字幕工具箱) v3.0

**Subtitle Toolbox** 是一款专为字幕组、翻译者及教育工作者设计的高效率自动化脚本工具。v3.0 版本进行了底层架构重构，实现了 UI 与逻辑的彻底解耦，极大提升了程序的稳定性和扩展性。

---

## ✨ v3.0 重大更新说明 (2025-11-28)

### 🏗️ 架构重组 (Architecture Refactoring)

* **Controller 模式**：引入了多重继承的控制器架构。将原本臃肿的 `app_controller` 拆分为：
* `BaseController`: 负责变量初始化与配置持久化。
* `UIController`: 处理路径浏览、界面反馈及预设切换逻辑。
* `TaskController`: 核心任务流执行（ASS/PDF/Word 生成）。
* `ToolController`: 快捷工具箱逻辑（文件合并）。


* **模块化解耦**：
* `control/`: 存放所有业务控制器。
* `function/`: 存放纯工具函数（文件名清理、重命名、通用工具）。
* `gui/`: 界面组件化，采用 `[name]_gui.py` 命名规范。



### 🎨 UI/UX 优化

* **视觉增强**：调大了模式切换器（SegmentedButton）的字体和高度，操作更清晰。
* **动态反馈**：路径输入框支持实时颜色验证（合法为绿，非法为红）。
* **日志系统**：针对不同任务类型（Word/PDF/ASS）引入了多色日志标签，方便快速定位任务状态。

### 📦 工业级打包

* **资源聚合**：规范了 PyInstaller 打包流程，支持全模块动态加载。
* **稳定性**：修复了在多层级目录（如 OpenFOAM 结构）下文件检索失效的问题。

---

## 📂 项目结构

```text
SubtitleToolbox/
├── control/              # 【核心大脑】业务控制器
│   ├── main_controller.py   # 总聚合类 (UnifiedApp)
│   ├── base_controller.py   # 基础设置
│   ├── ui_controller.py     # 界面交互
│   ├── task_controller.py   # 转换逻辑
│   └── tool_controller.py   # 合并工具
├── gui/                  # 【视觉层】UI 组件
│   ├── main_gui.py          # 主窗口
│   ├── ass_gui.py           # ASS 样式管理
│   ├── log_gui.py           # 日志系统
│   └── components_gui.py    # 工具箱面板
├── function/             # 【工具层】纯逻辑函数
│   ├── naming.py            # 重命名规则
│   ├── utils.py             # 通用处理
│   └── cleaners.py          # 文本清理
├── logic/                # 业务底层逻辑 (Word/PDF/TXT 处理)
├── font/                 # ASS 样式与字体处理
└── SubtitleToolbox.py    # 程序入口文件

```

---

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.10+ 及以下依赖库：

```bash
pip install customtkinter pypdf docx docxcompose pysubs2 pysrt send2trash pywin32 reportlab

```

### 2. 运行程序

```bash
python SubtitleToolbox.py

```

### 3. 打包 EXE

使用以下命令生成单文件绿色版：

```bash
python -m PyInstaller --noconfirm --onefile --windowed --name="SubtitleToolbox" --add-data "logic;logic" --add-data "control;control" --add-data "function;function" --add-data "gui;gui" --add-data "font;font" --add-data "config;config" --clean SubtitleToolbox.py

```

---

## 🛠️ 主要功能

* **ASS 转换**：支持中韩双语字幕样式自定义，批量生成 ASS 特效文件。
* **剧本生成**：一键将字幕导出为 Word (docx)、PDF 或 TXT 剧本，支持 4 合 1 分组模式。
* **快捷合并**：Word 批量合并（保留格式）、PDF 物理合并、TXT 文本串联。

---

## ⚖️ 许可证

基于 MIT License 开源。
