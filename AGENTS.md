# AGENTS.md

## Project Overview
**Heal-Jimaku (治幕)** - 字幕优化导出工具

利用大语言模型对多语言文本进行智能分割，将带有精确时间戳的 JSON 文件转换为自然、易读的 SRT 字幕文件。支持中文、英文、日文、韩文的智能断句处理。

## Tech Stack
- **Language**: Python 3.10-3.12
- **GUI Framework**: PyQt6
- **Package Manager**: uv
- **Shell Env**: Git Bash
- **主要依赖**:
  - `PyQt6` - GUI 框架
  - `requests` - HTTP 请求
  - `mutagen` - 音频元数据处理
  - `langdetect` - 语言检测
  - `gradio_client` - PDF 文档 OCR 处理
  - `python-docx` - Word 文档处理
  - `pyinstaller` - 打包工具（仅开发需要）

## Project Structure
```
heal-jimaku/
├── src/                          # 源代码目录
│   ├── main.py                   # 应用入口，初始化和主窗口启动
│   ├── config.py                 # 配置常量和默认值定义
│   ├── core/                     # 核心业务逻辑
│   │   ├── data_models.py        # 数据模型定义
│   │   ├── dots_ocr.py           # OCR 服务集成
│   │   ├── elevenlabs_api.py     # ElevenLabs API 集成
│   │   ├── llm_api.py            # LLM API 调用（支持多种格式）
│   │   ├── soniox_api.py         # Soniox API 集成
│   │   ├── srt_processor.py      # SRT 字幕处理核心逻辑
│   │   └── transcription_parser.py # 转录结果解析器
│   ├── ui/                       # 用户界面
│   │   ├── main_window.py        # 主窗口
│   │   ├── settings_dialog.py    # 设置对话框
│   │   ├── llm_advanced_settings_dialog.py  # LLM 高级设置
│   │   ├── cloud_transcription_dialog.py    # 云端转录对话框
│   │   ├── free_transcription_dialog.py     # 免费转录对话框
│   │   ├── background_settings_dialog.py    # 背景设置对话框
│   │   ├── background_manager.py # 背景管理器
│   │   ├── conversion_worker.py  # 转换工作线程
│   │   ├── custom_widgets.py     # 自定义控件
│   │   └── controllers/          # 控制器
│   │       └── conversion_controller.py  # 转换控制器
│   └── utils/                    # 工具函数
│       ├── file_utils.py         # 文件操作工具
│       ├── migration.py          # 数据迁移工具
│       └── user_friendly_logger.py # 用户友好日志
├── assets/                       # 静态资源
│   ├── fonts/                    # 字体文件
│   ├── background/               # 背景图片
│   └── *.png, *.ico              # 图标和截图
├── samples/                      # 示例文件
│   ├── en/                       # 英文示例
│   ├── ja/                       # 日文示例
│   └── zh/                       # 中文示例
├── docs/                         # 文档
│   └── USAGE.md                  # 使用说明
├── packaging/                    # 打包相关
│   ├── build_heal_jimaku.bat     # Windows 打包脚本
│   └── file_version_info.txt     # 版本信息
├── requirements.txt              # 依赖列表
└── README.md                     # 项目说明
```

## Key Modules

### Core 模块
- **srt_processor.py**: SRT 字幕处理核心，包含智能分割、时间戳处理、字幕生成
- **llm_api.py**: LLM API 封装，支持 OpenAI/Claude/Gemini/DeepSeek 等多种格式
- **transcription_parser.py**: 支持多种 ASR 服务商格式（ElevenLabs, Soniox, Whisper, Deepgram, AssemblyAI）
- **elevenlabs_api.py / soniox_api.py**: 云端转录服务集成

### UI 模块
- **main_window.py**: 主窗口，包含文件选择、格式配置、处理控制
- **llm_advanced_settings_dialog.py**: LLM 多配置管理
- **cloud_transcription_dialog.py**: Soniox/ElevenLabs 云端转录界面

### Config 模块
- **config.py**: 所有配置常量、默认值、键名定义
- 用户配置存储在 `~/.heal_jimaku/config/config.json`

## Development Setup
```bash
# 创建虚拟环境并安装依赖
uv venv
source .venv/Scripts/activate  # Windows Git Bash
uv pip install -r requirements.txt

# 运行应用
python src/main.py
```

## Code Style
- 使用 ruff 进行代码格式化和 lint
- 使用 ty 进行类型检查
- 函数和类需要添加 docstring
- 变量命名使用 snake_case

## Testing
- 测试文件放在 `tests/` 目录
- 测试文件命名: `test_*.py`
- 使用 pytest 运行测试

## Git Workflow
- 主分支: main
- 提交信息格式: `<type>: <description>`
- type: feat, fix, docs, refactor, test, chore

## Notes for AI Agents
- 优先使用 uv 管理依赖，不要使用 pip
- Windows 环境下激活虚拟环境: `source .venv/Scripts/activate`
- 处理路径时注意 Windows 兼容性，使用 pathlib
- 配置常量定义在 `src/config.py`，修改默认值时注意同步更新
- UI 组件使用 PyQt6，注意信号槽机制
- LLM API 支持多种格式，新增 API 时参考 `llm_api.py` 中的实现
