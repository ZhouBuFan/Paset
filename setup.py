"""
py2app setup script for Paset
"""

from setuptools import setup

APP = ['paset.py']
DATA_FILES = ['paset.png']
OPTIONS = {
    'argv_emulation': False,
    'packages': ['PyQt6', 'qfluentwidgets', 'AppKit'],
    'includes': ['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'qfluentwidgets'],
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'pandas', 'PyQt5'],
    'iconfile': 'assets/icon.icns',
    'plist': {
        'CFBundleName': 'Paset',
        'CFBundleDisplayName': 'Paset',
        'CFBundleIdentifier': 'com.paset.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.15',
        'LSUIElement': False,
        'NSHighResolutionCapable': True,
    }
}

setup(
    name='Paset',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
