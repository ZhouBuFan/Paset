#!/usr/bin/env python3
"""
Paset - macOS 剪贴板历史管理应用 (PyQt6 Fluent Design)
"""

import sys
import json
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidgetItem, QLabel, QSystemTrayIcon, QMenu,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon, QFont, QAction, QColor, QPixmap

from qfluentwidgets import (
    setTheme, Theme, FluentWindow,
    LineEdit, PushButton, PillPushButton, ToolButton,
    ListWidget, BodyLabel, CaptionLabel,
    CardWidget, IconWidget, VerticalSeparator,
    FluentIcon, InfoBar, InfoBarPosition,
    RoundMenu, Action, SmoothScrollArea,
    setCustomStyleSheet
)

from AppKit import NSPasteboard, NSStringPboardType


class ClipboardItem:
    def __init__(self, content, item_type="text", preview=None):
        self.id = int(datetime.now().timestamp() * 1000)
        self.content = content
        self.type = item_type
        self.preview = preview or (content[:100] if content else "")
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "type": self.type,
            "preview": self.preview,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        item = cls(data["content"], data.get("type", "text"), data.get("preview"))
        item.id = data["id"]
        item.created_at = data.get("created_at", datetime.now().isoformat())
        return item


class HistoryListItem(CardWidget):
    """自定义历史记录列表项卡片"""
    
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.item_data = item
        self.setFixedHeight(72)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 主布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)
        
        # 类型图标
        self.icon_label = IconWidget(self)
        self.icon_label.setFixedSize(32, 32)
        if item.type == "url":
            self.icon_label.setIcon(FluentIcon.LINK)
        elif item.type == "image":
            self.icon_label.setIcon(FluentIcon.PHOTO)
        else:
            self.icon_label.setIcon(FluentIcon.DOCUMENT)
        layout.addWidget(self.icon_label)
        
        # 内容区域
        content_layout = QVBoxLayout()
        content_layout.setSpacing(2)
        
        # 预览文本
        self.preview_label = BodyLabel(item.preview)
        self.preview_label.setWordWrap(False)
        self.preview_label.setMaximumWidth(280)
        content_layout.addWidget(self.preview_label)
        
        # 时间
        self.time_label = CaptionLabel(self.format_time_ago(item.created_at))
        self.time_label.setTextColor(QColor(120, 120, 120), QColor(160, 160, 160))
        content_layout.addWidget(self.time_label)
        
        layout.addLayout(content_layout, 1)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(4)
        
        self.copy_btn = ToolButton(FluentIcon.COPY)
        self.copy_btn.setFixedSize(36, 36)
        self.copy_btn.setIconSize(QSize(16, 16))
        self.copy_btn.setToolTip("复制")
        btn_layout.addWidget(self.copy_btn)
        
        self.delete_btn = ToolButton(FluentIcon.DELETE)
        self.delete_btn.setFixedSize(36, 36)
        self.delete_btn.setIconSize(QSize(16, 16))
        self.delete_btn.setToolTip("删除")
        btn_layout.addWidget(self.delete_btn)
        
        layout.addLayout(btn_layout)
    
    def format_time_ago(self, iso_string):
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
    
    def mouseDoubleClickEvent(self, event):
        self.copy_btn.click()


class PasetWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.items = []
        self.max_items = 100
        self.last_change_count = 0
        self.current_time_filter = None
        
        # 存储路径
        self.data_dir = os.path.expanduser("~/.paset")
        self.data_file = os.path.join(self.data_dir, "history.json")
        
        # 剪贴板
        self.pasteboard = NSPasteboard.generalPasteboard()
        self.last_change_count = self.pasteboard.changeCount()
        
        # 加载历史
        self.load_history()
        
        # 初始化UI
        self.init_ui()
        
        # 初始化托盘
        self.init_tray()
        
        # 开始监听剪贴板
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(500)
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("Paset")
        self.setFixedSize(480, 640)
        
        # 加载应用图标
        app_icon_path = os.path.join(os.path.dirname(__file__), "paset.png")
        if os.path.exists(app_icon_path):
            self.app_icon = QIcon(app_icon_path)
            self.setWindowIcon(self.app_icon)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # 标题
        title_layout = QHBoxLayout()
        title_icon = IconWidget(FluentIcon.PASTE)
        title_icon.setFixedSize(24, 24)
        title_layout.addWidget(title_icon)
        
        title_label = BodyLabel("剪贴板历史")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # 搜索框
        self.search_input = LineEdit()
        self.search_input.setPlaceholderText("搜索历史记录...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self.filter_items)
        layout.addWidget(self.search_input)
        
        # 时间筛选
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(6)
        
        self.time_buttons = {}
        time_filters = [
            ("全部", None),
            ("今天", "today"),
            ("昨天", "yesterday"),
            ("近7天", "7days"),
        ]
        
        for label, filter_key in time_filters:
            btn = PillPushButton(label)
            btn.setCheckable(True)
            if filter_key is None:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, fk=filter_key: self.on_time_filter_clicked(fk))
            self.time_buttons[filter_key] = btn
            filter_layout.addWidget(btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # 分隔线
        separator = VerticalSeparator()
        layout.addWidget(separator)
        
        # 列表
        self.list_widget = ListWidget()
        self.list_widget.setSpacing(4)
        layout.addWidget(self.list_widget, 1)
        
        # 底部操作栏
        bottom_layout = QHBoxLayout()
        
        self.status_label = CaptionLabel(f"共 {len(self.items)} 条记录")
        bottom_layout.addWidget(self.status_label)
        
        bottom_layout.addStretch()
        
        self.clear_btn = PushButton(FluentIcon.DELETE, "清空")
        self.clear_btn.clicked.connect(self.clear_all)
        bottom_layout.addWidget(self.clear_btn)
        
        layout.addLayout(bottom_layout)
        
        # 刷新列表
        self.refresh_list()
    
    def init_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # 使用应用图标
        app_icon_path = os.path.join(os.path.dirname(__file__), "paset.png")
        if os.path.exists(app_icon_path):
            self.tray_icon.setIcon(QIcon(app_icon_path))
        else:
            self.tray_icon.setIcon(QApplication.style().standardIcon(
                QApplication.style().StandardPixmap.SP_ComputerIcon
            ))
        
        self.tray_icon.setToolTip("Paset - 剪贴板历史")
        
        tray_menu = QMenu()
        
        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self.show_and_activate)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
    
    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_and_activate()
    
    def show_and_activate(self):
        if self.isHidden():
            self.setHidden(False)
        self.showNormal()
        self.raise_()
        self.activateWindow()
    
    def load_history(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.items = [ClipboardItem.from_dict(item) for item in data]
        except Exception as e:
            print(f"加载历史失败: {e}")
    
    def save_history(self):
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([item.to_dict() for item in self.items], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史失败: {e}")
    
    def check_clipboard(self):
        current_count = self.pasteboard.changeCount()
        if current_count != self.last_change_count:
            self.last_change_count = current_count
            self.extract_clipboard()
    
    def extract_clipboard(self):
        content = self.pasteboard.stringForType_(NSStringPboardType)
        if content:
            for i, item in enumerate(self.items):
                if item.content == content:
                    self.items.pop(i)
                    break
            
            item_type = "url" if self.is_url(content) else "text"
            new_item = ClipboardItem(content, item_type)
            self.items.insert(0, new_item)
            
            if len(self.items) > self.max_items:
                self.items = self.items[:self.max_items]
            
            self.save_history()
            self.refresh_list()
            
            InfoBar.success(
                title="已记录",
                content=f"{content[:30]}...",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
    
    def is_url(self, text):
        text = text.strip()
        return text.startswith("http://") or text.startswith("https://")
    
    def get_time_range(self, filter_type):
        now = datetime.now()
        if filter_type == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif filter_type == "yesterday":
            yesterday = now - timedelta(days=1)
            start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
            end = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
        elif filter_type == "7days":
            start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif filter_type == "30days":
            start = (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif filter_type == "custom":
            start = now - timedelta(days=1)
            end = now
        else:
            return None, None
        return start, end
    
    def parse_datetime(self, iso_string):
        try:
            return datetime.fromisoformat(iso_string)
        except:
            return datetime.now()
    
    def on_time_filter_clicked(self, filter_key):
        self.current_time_filter = filter_key
        for key, btn in self.time_buttons.items():
            btn.setChecked(key == filter_key)
        self.filter_items(self.search_input.text())
    
    def refresh_list(self, filter_text=""):
        self.list_widget.clear()
        
        filtered = self.items
        
        if self.current_time_filter:
            start, end = self.get_time_range(self.current_time_filter)
            if start and end:
                filtered = [item for item in filtered
                           if start <= self.parse_datetime(item.created_at) <= end]
        
        if filter_text:
            filtered = [item for item in filtered
                       if filter_text.lower() in item.content.lower()]
        
        for item in filtered:
            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(0, 68))
            
            widget = HistoryListItem(item)
            widget.copy_btn.clicked.connect(lambda checked, i=item: self.copy_item(i))
            widget.delete_btn.clicked.connect(lambda checked, i=item: self.delete_item(i))
            
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, widget)
        
        self.update_status()
    
    def filter_items(self, text):
        self.refresh_list(text)
    
    def copy_item(self, item):
        self.pasteboard.clearContents()
        self.pasteboard.setString_forType_(item.content, NSStringPboardType)
        self.last_change_count = self.pasteboard.changeCount()
        
        InfoBar.success(
            title="已复制",
            content=item.preview[:30],
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1500,
            parent=self
        )
    
    def delete_item(self, item):
        self.items = [i for i in self.items if i.id != item.id]
        self.save_history()
        self.refresh_list(self.search_input.text())
        
        InfoBar.info(
            title="已删除",
            content="记录已删除",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1500,
            parent=self
        )
    
    def clear_all(self):
        from qfluentwidgets import Dialog
        
        dialog = Dialog("确认清空", "确定要清空所有历史记录吗？此操作不可撤销。", self)
        dialog.setTitleBarIcon(FluentIcon.WARNING)
        
        if dialog.exec():
            self.items = []
            self.save_history()
            self.refresh_list()
            
            InfoBar.success(
                title="已清空",
                content="所有历史记录已清空",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
    
    def update_status(self):
        visible_count = self.list_widget.count()
        total_count = len(self.items)
        
        if visible_count == total_count:
            self.status_label.setText(f"共 {total_count} 条记录")
        else:
            self.status_label.setText(f"共 {total_count} 条 | 显示 {visible_count} 条")
    
    def quit_app(self):
        QApplication.quit()
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 自动跟随系统主题
    setTheme(Theme.AUTO)
    
    window = PasetWindow()
    window.show()
    
    sys.exit(app.exec())
