# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# 获取项目根目录
project_root = os.path.abspath(SPECPATH)
src_path = os.path.join(project_root, 'src')

a = Analysis(
    [os.path.join(src_path, 'auto_subtitle.py')],
    pathex=[src_path],  # 添加 src 到搜索路径
    binaries=[],
    datas=[
        (os.path.join(src_path, 'core'), 'core'),  # 打包 core 模块
        (os.path.join(src_path, 'config.py'), '.'),  # 打包 config.py
    ],
    hiddenimports=[
        'core.audio_extractor',
        'core.audio_processor',
        'core.subtitle_pipeline',
        'core.elevenlabs_api',
        'core.llm_api',
        'core.srt_processor',
        'core.transcription_parser',
        'core.data_models',
        'config',
        'av',
        'mutagen',
        'langdetect',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt6', 'PySide6', 'tkinter', 'matplotlib', 'ui'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='heal-jimaku-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
