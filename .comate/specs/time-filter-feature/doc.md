# Paset 时间筛选功能

## 1. 需求场景

用户需要按时间维度筛选剪贴板历史记录，例如：
- 查看今天、昨天、本周、本月的记录
- 方便快速定位近期复制的内容
- 避免在大量历史记录中手动翻找

## 2. 技术方案

### 2.1 功能设计

- **快捷时间筛选按钮**：今天、昨天、近7天、近30天
- **自定义日期范围**：开始日期和结束日期选择
- **与搜索框联动**：时间筛选 + 关键词搜索可以同时使用

### 2.2 界面设计

在搜索栏下方添加一行时间筛选控件：
```
┌─────────────────────────────────────┐
│ 🔍 搜索...                          │
├─────────────────────────────────────┤
│ [今天] [昨天] [近7天] [近30天] [📅] │
├─────────────────────────────────────┤
│ 📝 示例文本                    2分钟前│
│ 📝 另一条记录                  1小时前│
└─────────────────────────────────────┘
```

### 2.3 实现细节

1. **时间计算逻辑**：
   - 今天：00:00:00 到 23:59:59
   - 昨天：昨天 00:00:00 到昨天 23:59:59
   - 近7天：7天前 00:00:00 到现在
   - 近30天：30天前 00:00:00 到现在
   - 自定义：用户选择开始和结束日期

2. **数据结构**：
   - 每个 `ClipboardItem` 已有 `created_at` 字段（ISO 8601 格式）
   - 通过解析 `created_at` 进行时间比较

3. **UI 交互**：
   - 快捷按钮点击后高亮显示当前选中状态
   - 自定义日期通过 QDateEdit 控件选择
   - 筛选状态改变时自动刷新列表
   - 点击"全部"按钮清除时间筛选

## 3. 受影响文件

| 文件路径 | 操作类型 | 说明 |
|---------|---------|------|
| `paset.py` | 修改 | 主程序：添加时间筛选控件和过滤逻辑 |

## 4. 核心代码设计

### 4.1 时间计算工具函数

```python
def get_time_range(filter_type):
    now = datetime.now()
    if filter_type == 'today':
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif filter_type == 'yesterday':
        yesterday = now - timedelta(days=1)
        start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
    elif filter_type == '7days':
        start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif filter_type == '30days':
        start = (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    return start, end
```

### 4.2 筛选逻辑

```python
def filter_items(self):
    filter_text = self.search_input.text().lower()
    
    filtered = self.items
    
    # 时间筛选
    if self.current_time_filter:
        start, end = get_time_range(self.current_time_filter)
        filtered = [item for item in filtered 
                   if start <= datetime.fromisoformat(item.created_at) <= end]
    
    # 文本搜索
    if filter_text:
        filtered = [item for item in filtered 
                   if filter_text in item.content.lower()]
    
    return filtered
```

## 5. 边界条件

- 无历史记录时筛选按钮仍然可用但列表为空
- 自定义日期范围时，结束日期不能早于开始日期
- 切换筛选条件时保持搜索关键词不变
- 清除时间筛选后显示全部记录

## 6. 预期成果

1. 界面增加时间筛选按钮行
2. 点击快捷按钮按时间过滤列表
3. 支持与搜索关键词组合使用
4. UI 美观，交互流畅
