"""
py2app setup script for Paset
"""

from setuptools import setup

APP = ['paset.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['PyQt6', 'AppKit'],
    'includes': ['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'],
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'pandas'],
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
