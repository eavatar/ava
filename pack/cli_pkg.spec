# -*- mode: python -*-
# -*- coding: utf-8 -*-

lib_path = os.path.join('src', 'libs')
app_path = os.path.join('src', 'eavatar.ava')
res_path = os.path.join(app_path, 'res')


exe_name = 'ava'
hiddenimports = []
run_strip = False
run_upx = False
extra_binaries = []


if sys.platform.startswith('win32'):
    exe_name = 'ava.exe'
    app_icon = os.path.join(res_path, 'eavatar.ico')
    plat_name = 'ava-win32'
    run_strip = False
    extra_binaries.append( ('libsodium.dll', os.path.join(lib_path, 'libsodium.dll'), 'BINARY'))

elif sys.platform.startswith('linux'):
    plat_name = 'ava-linux'
    run_strip = True
    extra_binaries.append( ('libsodium.so.13', os.path.join(lib_path, 'libsodium.so.13.1.0'), 'BINARY'))

elif sys.platform.startswith('darwin'):
    plat_name = 'ava-osx'
    extra_binaries.append( ('libsodium.dylib', os.path.join(lib_path, 'libsodium.13.dylib'), 'BINARY'))

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

a = Analysis([os.path.join(app_path, 'avacli.py')],
             pathex=[app_path],
             hiddenimports=hiddenimports,
             hookspath=None,
             runtime_hooks=None,
             excludes=['PyQt4', 'wx', 'django', 'Tkinter', 'gi.repository', 'objc', 'AppKit', 'Foundation'])

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.dependencies,
          exclude_binaries=True,
          name=os.path.join('build', 'pyi.'+sys.platform, 'server', exe_name),
          debug=False,
          strip=run_strip,
          upx=run_upx,
          icon= os.path.join(res_path, 'eavatar.ico'),
          console=True )


coll = COLLECT(exe,
               a.binaries + extra_binaries,
               a.zipfiles,
               Tree(os.path.join(app_path, 'pod'), 'pod', excludes=['*.pyc']),
               Tree(res_path, 'res', excludes=['*.pyc']),
               a.datas,
#               shfile,
               strip=run_strip,
               upx=run_upx,
               name=os.path.join('dist', plat_name))

