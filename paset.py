#!/usr/bin/env python3
"""
Paset - macOS 剪贴板历史管理应用 (PyQt6 版本)
"""

import sys
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QLineEdit, QLabel,
    QMessageBox, QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont, QAction

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


class PasetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.items = []
        self.max_items = 100
        self.last_change_count = 0
        
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
        self.timer.start(500)  # 每0.5秒检查一次
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("Paset - 剪贴板历史")
        self.setGeometry(100, 100, 500, 600)
        
        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("📋 剪贴板历史")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索...")
        self.search_input.textChanged.connect(self.filter_items)
        layout.addWidget(self.search_input)
        
        # 列表
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.copy_selected)
        self.list_widget.setAlternatingRowColors(True)
        layout.addWidget(self.list_widget)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.copy_btn = QPushButton("复制选中")
        self.copy_btn.clicked.connect(self.copy_selected)
        button_layout.addWidget(self.copy_btn)
        
        self.delete_btn = QPushButton("删除选中")
        self.delete_btn.clicked.connect(self.delete_selected)
        button_layout.addWidget(self.delete_btn)
        
        self.clear_btn = QPushButton("清空全部")
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)
        
        layout.addLayout(button_layout)
        
        # 状态栏
        self.status_label = QLabel()
        self.update_status()
        layout.addWidget(self.status_label)
        
        # 刷新列表
        self.refresh_list()
    
    def init_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        # 使用默认图标
        self.tray_icon.setIcon(self.style().standardIcon(
            self.style().StandardPixmap.SP_ComputerIcon
        ))
        self.tray_icon.setToolTip("Paset - 剪贴板历史")
        
        # 托盘菜单
        tray_menu = QMenu()
        
        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self.show_and_activate)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
    
    def on_tray_activated(self, reason):
        """托盘图标点击"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_and_activate()
    
    def show_and_activate(self):
        """显示并激活窗口"""
        self.show()
        self.raise_()
        self.activateWindow()
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.items = [ClipboardItem.from_dict(item) for item in data]
        except Exception as e:
            print(f"加载历史失败: {e}")
    
    def save_history(self):
        """保存历史记录"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([item.to_dict() for item in self.items], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史失败: {e}")
    
    def check_clipboard(self):
        """检查剪贴板变化"""
        current_count = self.pasteboard.changeCount()
        
        if current_count != self.last_change_count:
            self.last_change_count = current_count
            self.extract_clipboard()
    
    def extract_clipboard(self):
        """提取剪贴板内容"""
        content = self.pasteboard.stringForType_(NSStringPboardType)
        
        if content:
            # 检查是否已存在
            for i, item in enumerate(self.items):
                if item.content == content:
                    self.items.pop(i)
                    break
            
            # 判断类型
            item_type = "url" if self.is_url(content) else "text"
            
            # 创建新记录
            new_item = ClipboardItem(content, item_type)
            self.items.insert(0, new_item)
            
            # 限制数量
            if len(self.items) > self.max_items:
                self.items = self.items[:self.max_items]
            
            self.save_history()
            self.refresh_list()
    
    def is_url(self, text):
        """检查是否为URL"""
        text = text.strip()
        return text.startswith("http://") or text.startswith("https://")
    
    def refresh_list(self, filter_text=""):
        """刷新列表"""
        self.list_widget.clear()
        
        filtered = self.items
        if filter_text:
            filtered = [item for item in self.items 
                       if filter_text.lower() in item.content.lower()]
        
        for item in filtered:
            type_icon = "📝" if item.type == "text" else "🔗"
            display_text = f"{type_icon} {item.preview}"
            
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.ItemDataRole.UserRole, item.id)
            self.list_widget.addItem(list_item)
        
        self.update_status()
    
    def filter_items(self, text):
        """过滤列表"""
        self.refresh_list(text)
    
    def get_selected_item(self):
        """获取选中项"""
        current = self.list_widget.currentItem()
        if current:
            item_id = current.data(Qt.ItemDataRole.UserRole)
            for item in self.items:
                if item.id == item_id:
                    return item
        return None
    
    def copy_selected(self):
        """复制选中项"""
        item = self.get_selected_item()
        if item:
            self.pasteboard.clearContents()
            self.pasteboard.setString_forType_(item.content, NSStringPboardType)
            self.last_change_count = self.pasteboard.changeCount()
            self.status_label.setText("✓ 已复制!")
    
    def delete_selected(self):
        """删除选中项"""
        item = self.get_selected_item()
        if item:
            self.items = [i for i in self.items if i.id != item.id]
            self.save_history()
            self.refresh_list(self.search_input.text())
    
    def clear_all(self):
        """清空全部"""
        reply = QMessageBox.question(
            self, "确认", "确定要清空所有历史记录吗?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.items = []
            self.save_history()
            self.refresh_list()
    
    def update_status(self):
        """更新状态栏"""
        self.status_label.setText(f"共 {len(self.items)} 条记录")
    
    def quit_app(self):
        """退出应用"""
        QApplication.quit()
    
    def closeEvent(self, event):
        """关闭窗口时隐藏到托盘"""
        event.ignore()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    window = PasetWindow()
    window.show()
    
    sys.exit(app.exec())
