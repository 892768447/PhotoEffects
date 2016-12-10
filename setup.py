# -*- coding: utf-8 -*-
# windows 无控制台
# console  有控制台

from distutils.core import setup
import sys
import py2exe    # @UnusedImport

sys.argv.append("py2exe")    # 允许程序通过双击的形式执行

if sys.version_info.major >= 3.0:
    opt_bundle_files = 0
else:
    opt_bundle_files = 1

includes = [
    "lib", "widget",
    "sip", "PyQt5.QtCore",
    "PyQt5.QtGui", "PyQt5.QtWidgets",
    "PyQt5.QtPrintSupport",
    "PyQt5.QtWebKit",
    "PyQt5.QtWebKitWidgets",
    "PyQt5.QtNetwork"
]

dll_excludes = ["MSVCP90.dll"]

# compressed 为1 则压缩文件
# optimize 为优化级别 默认为0
options = {
    "py2exe":{
        "compressed":1,
        "optimize":2,
        "includes":includes,
        "dll_excludes":dll_excludes,
        "bundle_files": 1
    }
}

setup(
    version = "1.0.0",
    description = "WDDF",
    name = "WDDF",
    zipfile = None,
    options = options,
    windows = [{"script": "main.py", "icon_resources": [(1, "app/icon.ico")]}]
)
