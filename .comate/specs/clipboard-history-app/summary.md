# Paset - macOS 剪贴板历史应用开发总结

## 项目概述

使用 Electron 创建了一个 macOS 剪贴板历史管理应用。

## 技术栈
- **Electron** - 跨平台桌面应用框架
- **electron-store** - 本地持久化存储

## 项目结构
```
Paset/
├── package.json      # 项目配置
├── main.js           # 主进程（剪贴板监听、托盘、存储）
├── index.html        # 渲染进程（UI界面）
└── assets/           # 资源文件
```

## 核心功能
- **剪贴板监听**：每 0.5 秒检测剪贴板变化
- **多类型支持**：文本、URL、图片
- **历史管理**：搜索、删除、清空
- **快速复制**：双击或点击按钮复制
- **菜单栏应用**：不显示在 Dock
- **本地存储**：数据持久化

## 运行方式

```bash
cd /Users/alex/Desktop/AlexWork/Paset
npm start
```

应用启动后会在菜单栏显示图标，点击即可查看剪贴板历史。
