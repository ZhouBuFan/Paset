# Paset - macOS Clipboard History Manager

[中文文档](README_CN.md)

A lightweight macOS clipboard history manager that automatically records your copied content for easy access.

## Features

- Automatically monitors and records clipboard content (text, URLs)
- Quick search through history
- Double-click or button click to copy history items
- System tray icon - hides to tray when window is closed
- Local storage - your data stays on your computer

## System Requirements

- macOS 10.15 or later
- Python 3.10+ (for building only)

## Usage

### Run the Compiled App

1. Double-click `dist/Paset.app` to launch
2. Drag to Applications folder for permanent use
3. First run may require permission in "System Preferences → Privacy & Security"

### Operations

- **Copy Content**: App automatically records copied text
- **View History**: See all records in the list
- **Search**: Type keywords in search box to filter
- **Re-copy**: Double-click item or select and click "Copy Selected"
- **Delete**: Select item and click "Delete Selected"
- **Clear All**: Click "Clear All"
- **Close Window**: App hides to system tray
- **Show Window**: Click tray icon
- **Quit**: Right-click tray icon → Quit

---

## How to Build

### 1. Create Virtual Environment

```bash
cd /path/to/Paset
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install PyQt6 pyobjc-framework-Cocoa py2app
```

### 3. Build App

```bash
rm -rf build
python setup.py py2app
```

The compiled app will be at `dist/Paset.app`.

---

## How to Change Icon

### Method 1: Generate with Script

1. Edit `create_icon.py`:
   ```python
   painter.setBrush(QColor("#007AFF"))  # Change background color
   painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "P")  # Change text
   ```

2. Run the script:
   ```bash
   source venv/bin/activate
   python create_icon.py
   ```

3. Generate icns file:
   ```bash
   mkdir -p assets/icon.iconset
   cp assets/icon_16.png assets/icon.iconset/icon_16x16.png
   cp assets/icon_32.png assets/icon.iconset/icon_16x16@2x.png
   cp assets/icon_32.png assets/icon.iconset/icon_32x32.png
   cp assets/icon_64.png assets/icon.iconset/icon_32x32@2x.png
   cp assets/icon_128.png assets/icon.iconset/icon_128x128.png
   cp assets/icon_256.png assets/icon.iconset/icon_128x128@2x.png
   cp assets/icon_256.png assets/icon.iconset/icon_256x256.png
   cp assets/icon_512.png assets/icon.iconset/icon_256x256@2x.png
   cp assets/icon_512.png assets/icon.iconset/icon_512x512.png
   sips -s format png assets/icon_512.png --out assets/icon.iconset/icon_512x512@2x.png
   iconutil -c icns assets/icon.iconset -o assets/icon.icns
   ```

4. Rebuild the app

### Method 2: Use Custom Icon

1. Prepare a 1024x1024 PNG image

2. Create icns:
   ```bash
   mkdir -p assets/icon.iconset
   sips -z 16 16     your_icon.png --out assets/icon.iconset/icon_16x16.png
   sips -z 32 32     your_icon.png --out assets/icon.iconset/icon_16x16@2x.png
   sips -z 32 32     your_icon.png --out assets/icon.iconset/icon_32x32.png
   sips -z 64 64     your_icon.png --out assets/icon.iconset/icon_32x32@2x.png
   sips -z 128 128   your_icon.png --out assets/icon.iconset/icon_128x128.png
   sips -z 256 256   your_icon.png --out assets/icon.iconset/icon_128x128@2x.png
   sips -z 256 256   your_icon.png --out assets/icon.iconset/icon_256x256.png
   sips -z 512 512   your_icon.png --out assets/icon.iconset/icon_256x256@2x.png
   sips -z 512 512   your_icon.png --out assets/icon.iconset/icon_512x512.png
   sips -z 1024 1024 your_icon.png --out assets/icon.iconset/icon_512x512@2x.png
   iconutil -c icns assets/icon.iconset -o assets/icon.icns
   ```

3. Rebuild the app

---

## Project Structure

```
Paset/
├── paset.py           # Main source code
├── setup.py           # py2app build config
├── create_icon.py     # Icon generation script
├── assets/
│   ├── icon.icns      # App icon
│   └── icon.iconset/  # Icon source files
├── venv/              # Python virtual environment
├── dist/
│   └── Paset.app      # Compiled application
├── README.md          # English documentation
└── README_CN.md       # Chinese documentation
```

## Data Storage

Clipboard history is stored at:
```
~/.paset/history.json
```

## Development

Run without compiling:
```bash
source venv/bin/activate
python paset.py
```

## FAQ

**Q: "Cannot be opened because it is from an unidentified developer"**

A: Right-click the app → Select "Open" → Click "Open" to confirm. Or allow in "System Preferences → Privacy & Security".

**Q: Icon not updated**

A: macOS caches icons. Try:
```bash
sudo rm -rf /Library/Caches/com.apple.iconservices.store
touch dist/Paset.app
```

**Q: App not recording clipboard**

A: Ensure app is running (check system tray). May need to grant Accessibility permission.

## License

MIT License
