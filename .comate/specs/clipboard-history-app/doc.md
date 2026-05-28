# macOS 剪贴板历史记录应用 (Paset)

## 1. 需求场景

用户需要一个 macOS 本地应用，能够：
- 自动监听系统剪贴板的变化
- 记录所有复制的内容（文本、图片、文件路径等）
- 提供历史记录列表供查看和快速访问
- 点击历史记录可重新复制到剪贴板
- 数据本地存储，保护隐私

## 2. 技术方案

### 2.1 技术栈
- **语言**: Swift 5.9+
- **UI 框架**: SwiftUI
- **最低支持版本**: macOS 13.0 (Ventura)
- **存储**: UserDefaults + 文件系统（图片等二进制数据）
- **架构**: MVVM

### 2.2 核心技术
- `NSPasteboard` - 访问系统剪贴板
- `Timer` - 轮询检测剪贴板变化
- `NSStatusBar` - 菜单栏图标和菜单
- `FileManager` - 持久化存储

### 2.3 应用架构

```
Paset/
├── PasetApp.swift          # 应用入口
├── Models/
│   ├── ClipboardItem.swift # 剪贴板数据模型
│   └── ContentType.swift   # 内容类型枚举
├── ViewModels/
│   └── ClipboardViewModel.swift # 业务逻辑
├── Views/
│   ├── ContentView.swift   # 主界面
│   ├── HistoryListView.swift    # 历史列表
│   ├── ClipboardItemView.swift  # 单条记录视图
│   └── SettingsView.swift       # 设置界面
├── Services/
│   ├── ClipboardMonitor.swift   # 剪贴板监听服务
│   └── StorageService.swift     # 存储服务
├── Resources/
│   └── Assets.xcassets    # 图标等资源
└── Info.plist             # 权限配置
```

## 3. 核心功能设计

### 3.1 ClipboardItem 数据模型

```swift
struct ClipboardItem: Identifiable, Codable {
    let id: UUID
    let content: Data          // 内容数据
    let contentType: ContentType
    let preview: String        // 预览文本
    let createdAt: Date
    let sourceApp: String?     // 来源应用
}

enum ContentType: String, Codable {
    case text
    case url
    case image
    case file
}
```

### 3.2 ClipboardMonitor - 剪贴板监听

```swift
class ClipboardMonitor: ObservableObject {
    private var timer: Timer?
    private var lastChangeCount: Int
    private let pasteboard = NSPasteboard.general
    
    @Published var items: [ClipboardItem] = []
    
    func startMonitoring() {
        timer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { [weak self] _ in
            self?.checkForChanges()
        }
    }
    
    private func checkForChanges() {
        guard pasteboard.changeCount != lastChangeCount else { return }
        lastChangeCount = pasteboard.changeCount
        // 提取并保存新内容
    }
}
```

### 3.3 菜单栏应用

应用运行在菜单栏，不显示在 Dock：
- 菜单栏图标：剪贴板图标
- 点击显示历史列表
- 支持搜索过滤
- 设置：开机启动、最大记录数、清除历史

### 3.4 存储策略

- 文本内容：直接存储到 UserDefaults（JSON 编码）
- 图片：存储到应用沙盒的 Documents 目录
- 最大记录数：默认 100 条，可配置
- 自动清理：超过限制时删除最旧记录

## 4. 受影响文件

| 文件路径 | 操作类型 | 说明 |
|---------|---------|------|
| Paset.xcodeproj | 新建 | Xcode 项目文件 |
| Paset/PasetApp.swift | 新建 | 应用入口 |
| Paset/Models/ClipboardItem.swift | 新建 | 数据模型 |
| Paset/Models/ContentType.swift | 新建 | 类型枚举 |
| Paset/ViewModels/ClipboardViewModel.swift | 新建 | 视图模型 |
| Paset/Services/ClipboardMonitor.swift | 新建 | 监听服务 |
| Paset/Services/StorageService.swift | 新建 | 存储服务 |
| Paset/Views/ContentView.swift | 新建 | 主界面 |
| Paset/Views/HistoryListView.swift | 新建 | 历史列表 |
| Paset/Views/ClipboardItemRow.swift | 新建 | 记录行视图 |
| Paset/Views/SettingsView.swift | 新建 | 设置界面 |
| Paset/Resources/Assets.xcassets | 新建 | 资源文件 |
| Paset/Info.plist | 新建 | 权限配置 |

## 5. 边界条件和异常处理

### 5.1 剪贴板访问
- 检查剪贴板权限状态
- 处理空剪贴板情况
- 处理超大内容（限制单条最大 10MB）

### 5.2 存储异常
- 磁盘空间不足处理
- 数据损坏恢复机制
- 编码/解码失败处理

### 5.3 性能考虑
- 图片压缩存储
- 预览文本截断（最多 200 字符）
- 列表虚拟化（大量记录时）

## 6. 数据流

```
用户复制 → 系统剪贴板
    ↓
ClipboardMonitor 检测变化 (轮询 0.5s)
    ↓
提取内容 → 判断类型 → 创建 ClipboardItem
    ↓
StorageService 持久化
    ↓
更新 ViewModel @Published items
    ↓
SwiftUI 刷新 UI
```

## 7. 预期成果

1. **菜单栏应用**：常驻菜单栏，点击显示历史
2. **自动记录**：复制内容自动保存到历史
3. **快速访问**：点击历史项即可复制
4. **搜索功能**：快速查找历史记录
5. **本地存储**：数据不离开设备，保护隐私
6. **可配置**：最大记录数、开机启动等设置

## 8. 后续扩展（可选）

- [ ] 快捷键快速唤起
- [ ] 支持更多内容类型（富文本、文件）
- [ ] 分组/标签功能
- [ ] iCloud 同步
- [ ] 加密存储
