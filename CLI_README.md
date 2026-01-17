# 命令行字幕生成工具

独立的命令行工具，完全不依赖 GUI，实现视频自动生成字幕的完整流程。

## 功能特点

- ✅ **完全独立** - 不依赖 PyQt6 和 GUI 组件
- ✅ **自动化流程** - 一条命令完成所有步骤
- ✅ **智能分割** - 自动将长音频分割为 28 分钟片段（避开 ElevenLabs 30分钟限制）
- ✅ **多种转录方式** - 支持 ElevenLabs API（推荐）或免费版（已失效）
- ✅ **配置复用** - 自动读取 GUI 保存的配置
- ✅ **LLM 优化** - 使用大模型优化字幕断句
- ✅ **多语言支持** - 支持中文、日文、英文、韩文

## 工作流程

```
视频文件
  ↓
1. 提取音频 → OGG 编码
  ↓
2. 检查时长 → 分割为 28 分钟片段（如需要）
  ↓
3. ElevenLabs Web 转录 → 生成 JSON
  ↓
4. 合并多个 JSON（如有分割）
  ↓
5. LLM 优化断句 → 生成 SRT
  ↓
字幕文件（保存在视频同目录）
```

## 安装依赖

确保已安装所有必需的依赖：

```bash
pip install av requests mutagen langdetect
```

## 转录服务配置

### 三种转录方式

1. **ElevenLabs API（推荐）**
   - 需要注册账号获取 API Key
   - 稳定可靠，有免费额度
   - 在 GUI 中保存或通过命令行参数指定

2. **ElevenLabs Web 免费版**
   - 无需 API Key
   - **当前已失效**（返回 401 错误）
   - 不推荐使用

3. **Soniox API**
   - 仅 GUI 支持，命令行暂不支持

### 配置读取优先级

命令行参数 > GUI 配置文件（`~/.heal_jimaku/config/config.json`）

## 使用方法

### 基本使用（推荐）

在 GUI 中保存 API Key 后，命令行工具会自动读取：

```bash
# 自动使用 GUI 保存的配置
python src/auto_subtitle.py video.mp4

# 指定语言
python src/auto_subtitle.py video.mp4 --language ja
```

### 使用 ElevenLabs API Key

```bash
# 方式1: 临时指定（不保存到配置）
python src/auto_subtitle.py video.mp4 --elevenlabs-api-key YOUR_KEY

# 方式2: 在 GUI 中保存后直接使用
python src/auto_subtitle.py video.mp4
```

### 完整配置示例

```bash
# 同时指定 LLM 和 ElevenLabs API Key
python src/auto_subtitle.py video.mp4 \
  --llm-api-key sk-xxx \
  --elevenlabs-api-key el-xxx \
  --language ja

# 自定义分割时长
python src/auto_subtitle.py video.mp4 \
  --elevenlabs-api-key el-xxx \
  --max-duration 1500
```

支持的语言：
- `zh` - 中文
- `ja` - 日文
- `en` - 英文
- `ko` - 韩文

## 参数说明

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `video` | ✓ | - | 视频文件路径 |
| `--llm-api-key` | ✗ | 配置文件 | LLM API Key |
| `--elevenlabs-api-key` | ✗ | 配置文件 | ElevenLabs API Key（推荐） |
| `--api-url` | ✗ | 配置文件 | LLM API 地址 |
| `--model` | ✗ | 配置文件 | LLM 模型名称 |
| `--language` | ✗ | 自动检测 | 目标语言 (zh/ja/en/ko) |
| `--max-duration` | ✗ | 1680 | 音频分割最大时长（秒，28分钟） |
| `--temperature` | ✗ | 配置文件 | LLM 温度参数 |

**注意**: 
- 命令行参数会临时覆盖配置文件中的设置，但不会修改配置文件
- 推荐在 GUI 中保存 API Key，命令行工具会自动读取
- 无 ElevenLabs API Key 时会尝试免费版（已失效）

## 输出文件

工具会在视频文件同目录下生成：

- `video.srt` - 最终字幕文件
- 临时文件会自动清理（音频、JSON 等）

## 示例输出

```
[20:58:20] 开始处理视频: test.mp4
============================================================
[20:58:20] 步骤 1/5: 提取音频
[20:58:21]   提取进度: 50.0%
[20:58:22]   提取进度: 100.0%
[20:58:22] ✓ 音频提取完成: /tmp/test_extracted.ogg
============================================================
[20:58:22] 步骤 2/5: 检查音频时长并分割
[20:58:22]   音频时长: 2138.1秒 (35.6分钟)
[20:58:22]   最大时长限制: 1680秒 (28.0分钟)
[20:58:22]   音频超过限制，开始分割...
[20:58:23] ✓ 音频已分割为 2 个片段
============================================================
[20:58:23] 步骤 3/5: ElevenLabs 转录
[20:58:23]   [1/2] 转录: test_extracted_part001.ogg (1680.0秒)
[20:59:15]   ✓ 已保存: test_extracted_part001.json
[20:59:15]   [2/2] 转录: test_extracted_part002.ogg (458.1秒)
[20:59:45]   ✓ 已保存: test_extracted_part002.json
[20:59:45] ✓ 转录完成，生成 2 个JSON文件
============================================================
[20:59:45] 步骤 4/5: 合并转录结果
[20:59:45]   合并 2 个JSON文件...
[20:59:45] ✓ JSON合并完成: test_extracted_merged.json
============================================================
[20:59:45] 步骤 5/5: LLM优化并生成SRT
[20:59:45]   解析转录JSON...
[20:59:45]   ✓ 解析完成: 15234 个单词
[20:59:45]   调用LLM进行文本分割优化...
[21:00:12]   ✓ LLM分割完成: 856 个片段
[21:00:12]   生成SRT字幕...
[21:00:13]   ✓ 生成 856 条字幕
[21:00:13] ✓ SRT生成完成: test.srt
============================================================
[21:00:13] ✓ 全部完成！

============================================================
✓ 字幕已生成: test.srt
============================================================
```

## 故障排除

### 问题：音频提取失败
- 确保安装了 `av` 库：`pip install av`
- 检查视频文件是否损坏

### 问题：转录失败（401 Unauthorized）
- ElevenLabs 免费版已失效，需要使用 API Key
- 注册 ElevenLabs 账号获取 API Key：https://elevenlabs.io
- 在 GUI 中保存 API Key 或使用 `--elevenlabs-api-key` 参数

### 问题：LLM 调用失败
- 检查 API Key 是否正确
- 检查 API URL 是否可访问
- 确认账户有足够余额

## 与 GUI 版本的区别

| 特性 | GUI 版本 | 命令行版本 |
|------|----------|------------|
| 依赖 | PyQt6 | 无 GUI 依赖 |
| 使用方式 | 图形界面 | 命令行 |
| 调试 | 复杂（信号槽） | 简单（print） |
| 自动化 | 需手动操作 | 完全自动化 |
| 稳定性 | 可能有 Qt 相关问题 | 更稳定 |

## 技术细节

### 核心模块

- `subtitle_pipeline.py` - 流程编排（300+ 行）
- `auto_subtitle.py` - 命令行入口（130+ 行）

### 复用的核心库

- `core/audio_extractor.py` - 音频提取和分割
- `core/elevenlabs_api.py` - ElevenLabs API 客户端
- `core/llm_api.py` - LLM API 调用
- `core/srt_processor.py` - SRT 生成
- `core/transcription_parser.py` - JSON 解析

## 许可证

与主项目相同
