# Paset - macOS 剪贴板历史管理工具

[English](README.md)

一个轻量级的 macOS 剪贴板历史管理应用，自动记录你复制的内容，方便随时查看和再次使用。

## 功能特性

- 自动监听并记录剪贴板内容（文本、URL）
- 快速搜索历史记录
- 双击或点击按钮复制历史内容
- 系统托盘图标，关闭窗口后隐藏到托盘
- 本地存储，数据不会离开你的电脑

## 系统要求

- macOS 10.15 或更高版本
- Python 3.10+（仅编译时需要）

## 使用方法

### 直接运行编译好的应用

1. 双击 `dist/Paset.app` 启动应用
2. 可拖拽到"应用程序"文件夹永久使用
3. 首次运行可能需要在"系统偏好设置 → 隐私与安全性"中允许

### 应用操作

- **复制内容**：应用会自动记录你复制的文本
- **查看历史**：在列表中查看所有历史记录
- **搜索**：在搜索框输入关键词过滤
- **再次复制**：双击列表项或选中后点击"复制选中"
- **删除记录**：选中后点击"删除选中"
- **清空历史**：点击"清空全部"
- **关闭窗口**：点击关闭按钮，应用会隐藏到系统托盘
- **重新显示**：点击系统托盘图标
- **退出应用**：右键托盘图标 → 退出

---

## 如何编译

### 1. 创建虚拟环境

```bash
cd /path/to/Paset
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install PyQt6 pyobjc-framework-Cocoa py2app
```

### 3. 编译应用

```bash
rm -rf build
python setup.py py2app
```

编译完成后，应用位于 `dist/Paset.app`。

---

## 如何更换图标

### 方法一：使用脚本生成

1. 修改 `create_icon.py` 中的颜色和文字：
   ```python
   painter.setBrush(QColor("#007AFF"))  # 修改背景色
   painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "P")  # 修改显示文字
   ```

2. 运行图标生成脚本：
   ```bash
   source venv/bin/activate
   python create_icon.py
   ```

3. 重新生成 icns 文件：
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

4. 重新编译应用

### 方法二：使用自己的图标文件

1. 准备一个 1024x1024 的 PNG 图片

2. 创建 icns 文件：
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

3. 重新编译应用

---

## 项目结构

```
Paset/
├── paset.py           # 主程序源码
├── setup.py           # py2app 编译配置
├── create_icon.py     # 图标生成脚本
├── assets/
│   ├── icon.icns      # 应用图标
│   └── icon.iconset/  # 图标源文件
├── venv/              # Python 虚拟环境
├── dist/
│   └── Paset.app      # 编译后的应用
├── README.md          # 英文文档
└── README_CN.md       # 中文文档
```

## 数据存储

剪贴板历史数据存储在：
```
~/.paset/history.json
```

## 开发调试

不编译直接运行：
```bash
source venv/bin/activate
python paset.py
```

## 常见问题

**Q: 首次运行提示"无法打开，因为无法验证开发者"**

A: 右键点击应用 → 选择"打开" → 点击"打开"确认。或在"系统偏好设置 → 隐私与安全性"中允许运行。

**Q: 图标没有更新**

A: macOS 会缓存图标，尝试：
```bash
sudo rm -rf /Library/Caches/com.apple.iconservices.store
touch dist/Paset.app
```

**Q: 应用没有自动记录剪贴板**

A: 确保应用正在运行（检查系统托盘），可能需要授予辅助功能权限。

## License

MIT License
