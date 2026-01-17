# CLI 工具独立打包指南

## 打包命令

使用提供的批处理脚本：
```bash
build_cli.bat
```

或手动执行：
```bash
pyinstaller heal-jimaku-cli.spec --clean
```

## 测试打包结果

```bash
dist\heal-jimaku-cli.exe --help
```

## 打包说明

- **输出位置**: `dist\heal-jimaku-cli.exe`
- **预计大小**: ~50-80MB（无 Qt 依赖）
- **包含模块**: 
  - core 模块（音频处理、转录、LLM、SRT生成）
  - 必需依赖（av, requests, mutagen, langdetect）
- **排除模块**: PyQt6, PySide6, tkinter, matplotlib, ui

## 使用示例

```bash
# 基本使用
dist\heal-jimaku-cli.exe video.mp4

# 指定语言
dist\heal-jimaku-cli.exe video.mp4 --language ja

# 使用自定义 API
dist\heal-jimaku-cli.exe video.mp4 --api-key sk-xxx
```

## 故障排除

如果遇到 "No module named 'core'" 错误：
1. 确保使用 `heal-jimaku-cli.spec` 文件打包
2. 检查 spec 文件中的 `datas` 配置是否正确
3. 使用 `--clean` 参数清理旧的构建文件
