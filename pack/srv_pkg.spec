# -*- mode: python -*-
# -*- coding: utf-8 -*-

app_path = os.path.join('src', 'eavatar.ava')


exe_name = 'ava'
hiddenimports = []
run_strip = True

if sys.platform.startswith('win32'):
    exe_name = 'ava.exe'
    app_icon = os.path.join(app_path, 'res/eavatar.ico')
    ext_name = '.win'
    run_strip = False
    hiddenimports.append('depends_win32.py')
elif sys.platform.startswith('linux'):
    ext_name = '.lin'
    run_strip = True
    hiddenimports.append('depends_linux.py')
elif sys.platform.startswith('darwin'):
    ext_name = '.mac'
    hiddenimports.append('depends_osx.py')
else:
    ext_name = ''


a = Analysis([os.path.join(app_path,'avacli.py')],
             pathex=['src'],
             hiddenimports=hiddenimports,
             hookspath=None,
             runtime_hooks=None,
             excludes=['PyQt4', 'wx', 'django', 'Tkinter', 'gi.repository', 'objc', 'AppKit', 'Foundation'])

run_strip = False


pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.dependencies,
          exclude_binaries=True,
          name=os.path.join('build', 'pyi.'+sys.platform, 'server', exe_name),
          debug=False,
          strip=run_strip,
          upx=True,
          icon= os.path.join(app_path, 'home/static/images/eavatar.ico'),
          console=True )


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               Tree(os.path.join(app_path, 'home'), 'home', excludes=['*.pyc']),
               a.datas,
               strip=run_strip,
               upx=True,
               name=os.path.join('dist', 'ava'))

