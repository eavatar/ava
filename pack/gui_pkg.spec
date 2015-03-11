# -*- mode: python -*-
# -*- coding: utf-8 -*-

app_path = os.path.join('src', 'eavatar.ava')
app_icon = os.path.join(app_path, 'pod/static/eavatar.icns')

exe_name = 'avaw'
hiddenimports = []

run_strip = False
run_upx = True
console = False

if sys.platform == 'win32':
    exe_name = 'avaw.exe'
    app_icon = os.path.join(app_path, 'pod', 'static', 'eavatar.ico')
    ext_name = '.win'
elif sys.platform.startswith('linux'):
    ext_name = '.lin'
    run_strip = True
elif sys.platform.startswith('darwin'):
    ext_name = '.mac'
    run_upx = False
    # to hide the dock icon.
    console = True
else:
    ext_name = ''

# for copying data file according to PyInstaller's recipe
def Datafiles(*filenames, **kw):
    import os

    def datafile(path, strip_path=True):
        parts = path.split('/')
        path = name = os.path.join(*parts)
        if strip_path:
            name = os.path.basename(path)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    return TOC(
        datafile(filename, strip_path=strip_path)
        for filename in filenames
        if os.path.isfile(filename))

#shfile = Datafiles('pack/ava', '')

a = Analysis([os.path.join(app_path,'avagui.py')],
             pathex=['src'],
             hiddenimports=hiddenimports,
             hookspath=None,
             runtime_hooks=None,
             excludes=['PyQt4', 'wx', 'django', 'Tkinter', 'objc', 'AppKit', 'Foundation'])

run_strip = False
run_upx = False

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.dependencies,
          exclude_binaries=True,
          name=os.path.join('build', 'pyi.'+sys.platform, 'server', exe_name),
          debug=False,
          strip=run_strip,
          upx=run_upx,
          icon= os.path.join(app_path, 'pod/static/eavatar.ico'),
          console=console )


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               Tree(os.path.join(app_path, 'pod'), 'pod', excludes=['*.pyc']),
               a.datas,
#               shfile,
               strip=run_strip,
               upx=run_upx,
               name=os.path.join('dist', 'ava'))

if sys.platform.startswith('darwin'):
    app = BUNDLE(coll,
                name='Ava.app',
                appname='ava',
                icon=os.path.join(app_path, 'pod', 'static', 'eavatar.icns'))