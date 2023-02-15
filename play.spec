# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['play.py'],
             pathex=[],
             binaries=[],
             datas=[(r'Z:\标注\qss','qss'),
                (r'Z:\标注\img','img')],
             hiddenimports=['PySide6.QtCore','PySide6.QtGui','PySide6.QtWidgets'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['matplotlib','jedi','PIL','PySide6.QtNetwork'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='降雨视频分类',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='img/logo.ico',
          version="file_verison_info.txt")