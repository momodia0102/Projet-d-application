# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\Mohamed\\Desktop\\All_My_Files\\ALL _MY_Files\\INFO_SI\\PAPPl_INFOSI\\Robot_Modeler\\src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['OpenGL', 'OpenGL.GL', 'OpenGL.GLU', 'pyopengltk', 'matplotlib.backends.backend_tkagg', 'matplotlib.backends.backend_agg'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RobotModeler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RobotModeler',
)
