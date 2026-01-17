@echo off
REM CLI 工具打包脚本

echo 开始打包 CLI 工具...
echo.

REM 使用 spec 文件打包
pyinstaller heal-jimaku-cli.spec --clean

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo 打包成功！
    echo 可执行文件位置: dist\heal-jimaku-cli.exe
    echo ========================================
    echo.
    echo 测试命令:
    echo   dist\heal-jimaku-cli.exe --help
) else (
    echo.
    echo ========================================
    echo 打包失败！请检查错误信息
    echo ========================================
)

pause
