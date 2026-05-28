# Paset UI 美化升级

## 1. 需求场景

当前应用 UI 过于简陋，使用默认 Qt 样式，缺乏现代感。需要全面升级视觉设计，提升用户体验。

## 2. 技术方案

### 2.1 设计风格

- **设计语言**: 现代简洁，参考 macOS 原生应用风格
- **配色方案**: 深色主题为主，支持跟随系统切换
- **圆角风格**: 大圆角 (8-12px)，柔和现代
- **间距系统**: 统一的间距规范

### 2.2 具体改进

#### 整体框架
- 添加主窗口背景色和圆角
- 优化整体布局间距
- 添加窗口阴影效果

#### 标题栏
- 美化标题文字样式
- 添加应用图标
- 优化顶部区域背景

#### 搜索框
- 圆角搜索框
- 添加搜索图标
- 聚焦状态高亮
- 占位符文字样式

#### 时间筛选按钮
- 药丸形状 (pill) 按钮
- 选中状态蓝色背景+白色文字
- 未选中状态灰色背景
- 悬停效果

#### 列表项
- 卡片式列表项
- 显示内容预览+时间
- 悬停高亮效果
- 类型图标（彩色）
- 更好的时间格式化

#### 底部操作栏
- 统一按钮样式
- 状态栏信息清晰展示
- 分隔线样式

#### 系统托盘
- 使用应用自定义图标

### 2.3 配色方案 (Dark Mode)

```
背景色: #1E1E1E
卡片背景: #2D2D2D
边框色: #3D3D3D
主色调: #0A84FF (macOS Blue)
文字主色: #FFFFFF
文字次色: #98989D
成功色: #30D158
警告色: #FF453A
```

### 2.4 配色方案 (Light Mode)

```
背景色: #F5F5F7
卡片背景: #FFFFFF
边框色: #E5E5EA
主色调: #007AFF
文字主色: #000000
文字次色: #8E8E93
```

## 3. 受影响文件

| 文件路径 | 操作类型 | 说明 |
|---------|---------|------|
| `paset.py` | 修改 | 全面修改 UI 初始化、样式表、布局 |

## 4. 实现细节

### 4.1 QSS 样式表设计

```python
# 主窗口样式
window.setStyleSheet("""
    QMainWindow {
        background-color: #1E1E1E;
    }
""")

# 搜索框样式
QLineEdit {
    border: 1px solid #3D3D3D;
    border-radius: 8px;
    padding: 8px 12px;
    background-color: #2D2D2D;
    color: #FFFFFF;
    font-size: 13px;
}
QLineEdit:focus {
    border: 2px solid #0A84FF;
}

# 药丸按钮
QPushButton {
    border-radius: 14px;
    padding: 6px 16px;
    background-color: #3D3D3D;
    color: #FFFFFF;
    border: none;
    font-size: 12px;
}
QPushButton:checked {
    background-color: #0A84FF;
}
QPushButton:hover {
    background-color: #4D4D4D;
}

# 列表样式
QListWidget {
    border: none;
    background-color: transparent;
    outline: none;
}
QListWidget::item {
    border-radius: 8px;
    padding: 10px;
    margin: 2px 0;
    background-color: #2D2D2D;
}
QListWidget::item:hover {
    background-color: #3D3D3D;
}
QListWidget::item:selected {
    background-color: #0A84FF;
}
```

### 4.2 列表项渲染改进

当前列表项只显示图标+预览文字，改进后：
- 左侧：类型图标（更大、彩色）
- 中间：内容预览（主文字）+ 复制时间（次要文字）
- 右侧：快捷操作按钮（复制、删除）

### 4.3 时间格式化改进

```python
def format_time_ago(iso_string):
    dt = datetime.fromisoformat(iso_string)
    now = datetime.now()
    diff = now - dt
    
    if diff < timedelta(minutes=1):
        return "刚刚"
    elif diff < timedelta(hours=1):
        return f"{int(diff.seconds / 60)} 分钟前"
    elif diff < timedelta(days=1):
        return f"{int(diff.seconds / 3600)} 小时前"
    elif diff < timedelta(days=2):
        return "昨天"
    else:
        return dt.strftime("%m-%d %H:%M")
```

## 5. 边界条件

- 列表为空时的空状态美化
- 深色/浅色模式切换适配
- 高分辨率屏幕适配
- 长文本预览截断处理

## 6. 预期成果

1. 现代化、美观的 UI 界面
2. 与 macOS 风格协调的深色主题
3. 流畅的交互反馈（悬停、点击效果）
4. 清晰的信息层级和视觉层次
