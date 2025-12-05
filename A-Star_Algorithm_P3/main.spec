# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import sys
import os

# Absolute path to your project root (optional, helps if running spec from another folder)
project_root = os.path.abspath(os.path.dirname("."))

# Include all KV files and the components folder
datas = [
    (os.path.join(project_root, 'main.kv'), '.'),
    (os.path.join(project_root, 'app', 'screens', 'input', 'input_screen.kv'), 'app/screens/input'),
    (os.path.join(project_root, 'app', 'screens', 'ship', 'ship_screen.kv'), 'app/screens/ship'),
    (os.path.join(project_root, 'app', 'screens', 'error', 'error_screen.kv'), 'app/screens/error'),
    (os.path.join(project_root, 'app', 'components'), 'app/components'),
]

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=['win32timezone'],  # Needed for Kivy FileChooser on Windows
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,  # <-- datas are included here for PyInstaller onefile
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)
