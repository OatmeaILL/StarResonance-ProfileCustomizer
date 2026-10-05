# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os
import re
import UnityPy

with open('src/constants.py', 'r', encoding='utf-8') as f:
    content = f.read()
    match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', content)
    APP_VERSION = match.group(1) if match else 'unknown'

EXE_NAME = f'麦麦子名片头像修改工具 {APP_VERSION}'

unitypy_datas = collect_data_files('UnityPy')
unitypy_hiddenimports = collect_submodules('UnityPy')

# 显式包含 UnityPy/resources 目录(含 lzma.tpk)
# collect_data_files 在用户级 site-packages 环境下可能漏收 .tpk 文件,
# 导致打包后 EXE 启动报 FileNotFoundError: UnityPy\resources\lzma.tpk
unitypy_resources_dir = os.path.join(os.path.dirname(UnityPy.__file__), 'resources')
unitypy_datas = [(src, dst) for (src, dst) in unitypy_datas
                 if os.path.normpath(dst).lower() != os.path.normpath('UnityPy/resources').lower()]
unitypy_datas.append((unitypy_resources_dir, 'UnityPy/resources'))

src_hiddenimports = collect_submodules('src')

numpy_datas = collect_data_files('numpy')
archspec_datas = collect_data_files('archspec')

pil_hiddenimports = [
    'PIL.Image',
    'PIL.ImageEnhance',
    'PIL.PngImagePlugin',
    'PIL.JpegImagePlugin',
    'PIL.BmpImagePlugin',
    'PIL.TgaImagePlugin',
    'PIL.DdsImagePlugin',
    'PIL.TiffImagePlugin',
    # 用户可能通过"All files"选择 WebP/GIF，补回插件避免打包版加载失败
    'PIL.WebPImagePlugin',
    'PIL.GifImagePlugin',
    'PIL.ImageMode',
    'PIL.ImageFile',
    'PIL._typing',
    'PIL.ExifTags',
    'PIL.TiffTags',
    'PIL.JpegPresets',
    'PIL.ImageOps',
    'PIL.ImagePalette',
    'PIL.ImageChops',
    'PIL.ImageSequence',
    'PIL.GimpGradientFile',
    'PIL.GimpPaletteFile',
    'PIL.PaletteFile',
    'PIL._binary',
    'PIL._deprecate',
    'PIL._util',
    'psutil',
]

excludes_list = [
    'numpy.tests',
    'numpy.f2py',
    'numpy.typing.tests',
    'numpy.random.tests',
    'numpy.linalg.tests',
    'numpy.fft.tests',
    'numpy.lib.tests',
    'numpy.ma.tests',
    'numpy.polynomial.tests',
    'numpy._core.tests',
    'numpy.distutils',
    'numpy.conftest',
    'numpy._examples',
    'numpy.random._examples',
    'fsspec.implementations.smb',
    'fsspec.implementations.sftp',
    'fsspec.implementations.git',
    'fsspec.implementations.http',
    'fsspec.implementations.http_sync',
    'fsspec.implementations.webhdfs',
    'fsspec.implementations.jupyter',
    'fsspec.implementations.dask',
    'fsspec.implementations.arrow',
    'fsspec.implementations.dbfs',
    'fsspec.implementations.gist',
    'fsspec.implementations.github',
    'fsspec.implementations.libarchive',
    'fsspec.implementations.reference',
    'fsspec.implementations.zip',
    'fsspec.gui',
    'fsspec.fuse',
    'fsspec.conftest',
    'PIL.FpxImagePlugin',
    'PIL.MicImagePlugin',
    'PIL.SgiImagePlugin',
    'PIL.FitsImagePlugin',
    'PIL.SunImagePlugin',
    'PIL.IcnsImagePlugin',
    'PIL.IcoImagePlugin',
    'PIL.ImImagePlugin',
    'PIL.MpoImagePlugin',
    'PIL.MspImagePlugin',
    'PIL.PcxImagePlugin',
    'PIL.PdfImagePlugin',
    'PIL.PixarImagePlugin',
    'PIL.PsdImagePlugin',
    'PIL.QoiImagePlugin',
    'PIL.XpmImagePlugin',
    'PIL.XVThumbImagePlugin',
    'PIL.SpiderImagePlugin',
    'PIL.EpsImagePlugin',
    'PIL.FliImagePlugin',
    'PIL.GbrImagePlugin',
    'PIL.McIdasImagePlugin',
    'PIL.Hdf5StubImagePlugin',
    'PIL.BufrStubImagePlugin',
    'PIL.CurImagePlugin',
    'PIL.PalmImagePlugin',
    'PIL.ImtImagePlugin',
    'PIL.IptcImagePlugin',
    'PIL.Jpeg2KImagePlugin',
    'PIL.MpegImagePlugin',
    'PIL.WmfImagePlugin',
    'setuptools',
    # 注意: distutils 不能 exclude —— PyInstaller 6.x 内置 hook 需为它建立别名,
    # exclude 会导致 "already imported as ExcludedModule" 构建崩溃
    'lib2to3',
    # 以下为 fsspec(UnityPy依赖) 可选链条拖进来的无关重包:
    # fsspec/implementations/reference.py 延迟 import pandas, 8/24 起 pandas 被
    # pyaccess 带入环境, 导致 pandas+scipy+sqlalchemy+sqlite3 全家桶(约+48MB)被打包。
    # 项目纹理替换路径不使用它们, 明确排除:
    'pandas',
    'scipy',
    'pyaccess',
    'pyodbc',
    'sqlalchemy',
    'tkinter',
    'unittest',
    'doctest',
    'pydoc',
    'xmlrpc',
    'fcntl',
    'grp',
    'pwd',
    'posix',
    '_posixshmem',
    '_posixsubprocess',
    'resource',
    'termios',
    'readline',
    'curses',
    '_pyrepl',
    'java',
    'vms_lib',
    # PyQt5 多余模块（项目仅用 QtWidgets/QtCore/QtGui）
    'PyQt5.QtNetwork',
    'PyQt5.QtQuick',
    'PyQt5.QtQml',
    'PyQt5.QtQmlModels',
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebEngineCore',
    'PyQt5.QtWebChannel',
    'PyQt5.QtOpenGL',
    'PyQt5.QtPrintSupport',
    'PyQt5.QtSvg',
    'PyQt5.QtTest',
    'PyQt5.QtSql',
    'PyQt5.QtXml',
    'PyQt5.QtMultimedia',
    'PyQt5.QtMultimediaWidgets',
    'PyQt5.QtSerialPort',
    'PyQt5.QtDBus',
    'PyQt5.QtConcurrent',
    'PyQt5.QtBluetooth',
    'PyQt5.QtPositioning',
    'PyQt5.QtLocation',
    'PyQt5.QtSensors',
    'PyQt5.QtNfc',
    'PyQt5.QtCharts',
    'PyQt5.QtDataVisualization',
    # PIL 多余插件（项目仅用 Image/ImageEnhance，处理 PNG/JPG/BMP/TGA/DDS/TIFF）
    # 注意：ImageFont/ImageDraw/ImageDraw2/_imagingtk 必须保留，UnityPy 内部依赖
    'PIL._avif',
    'PIL.ImageQt',
    'PIL.ImageTk',
    'PIL.ImageCms',
    'PIL.ImageWin',
    'PIL.ImtImagePlugin',
    'PIL.IptcImagePlugin',
    'PIL.McIdasImagePlugin',
    # 其他无用模块
    'pydoc_data',
    'pdb',
    'profile',
    'pstats',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('image', 'image'),
    ] + unitypy_datas + numpy_datas + archspec_datas,
    hiddenimports=unitypy_hiddenimports + pil_hiddenimports + src_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes_list,
    noarchive=False,
)

# 过滤无用二进制文件（Qt 软件/ANGLE 渲染后端、QML 引擎、多余平台插件等）
# 项目仅用 QWidget(CPU渲染) + urllib，不依赖 OpenGL/QML/QtNetwork
exclude_bin_names = {
    'opengl32sw.dll',       # Qt 软件 OpenGL 渲染 (19.95MB)
    'd3dcompiler_47.dll',   # D3D 编译器 ANGLE 后端 (3.98MB)
    'libGLESv2.dll',        # OpenGL ES ANGLE 后端 (3.23MB)
    'libEGL.dll',           # EGL ANGLE 后端
    'Qt5Quick.dll',         # QML Quick (3.96MB)
    'Qt5Qml.dll',           # QML 引擎 (3.43MB)
    'Qt5QmlModels.dll',     # QML 模型
    'Qt5QmlWorkerScript.dll',
    'Qt5Network.dll',       # Qt 网络 (1.28MB) - 用 urllib
    'Qt5Svg.dll',           # SVG 渲染
    'Qt5PrintSupport.dll',  # 打印支持
    'Qt5WebEngine.dll',
    'Qt5WebEngineCore.dll',
    'Qt5WebEngineWidgets.dll',
    'Qt5WebChannel.dll',
    'Qt5OpenGL.dll',
    'Qt5Test.dll',
    'Qt5Sql.dll',
    'Qt5Xml.dll',
    'Qt5Multimedia.dll',
    'Qt5SerialPort.dll',
    'Qt5DBus.dll',
    'Qt5Concurrent.dll',
    'qminimal.dll',         # minimal 平台插件 (0.81MB)
    'qoffscreen.dll',       # offscreen 平台插件 (0.72MB)
    'qwebgl.dll',           # WebGL 平台插件
    'qtquick2plugin.dll',
    'qtqmlplugin.dll',
    'qsvg.dll',             # imageformats SVG 插件（Qt5Svg.dll 已排除，此插件无效）
    'qsvgicon.dll',         # iconengines SVG 插件（Qt5Svg.dll 已排除，此插件无效）
}
a.binaries = [b for b in a.binaries if os.path.basename(b[0]).lower() not in exclude_bin_names]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=EXE_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='image\\icon128.ico',
    version='version_info.txt',
)
