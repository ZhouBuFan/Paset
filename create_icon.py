#!/usr/bin/env python3
"""生成应用图标"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt6.QtCore import Qt, QRect
import sys
import os

def create_icon():
    # 创建不同尺寸的图标
    sizes = [16, 32, 64, 128, 256, 512]
    
    for size in sizes:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制圆角矩形背景
        margin = size // 16
        rect = QRect(margin, margin, size - 2*margin, size - 2*margin)
        
        # 渐变背景色
        painter.setBrush(QColor("#007AFF"))  # iOS 蓝
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, size // 5, size // 5)
        
        # 绘制剪贴板图标
        painter.setPen(QColor("white"))
        font = QFont("Arial", size // 2, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "P")
        
        painter.end()
        
        # 保存
        pixmap.save(f"/Users/alex/Desktop/AlexWork/Paset/assets/icon_{size}.png")
    
    print("图标已生成")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    create_icon()
