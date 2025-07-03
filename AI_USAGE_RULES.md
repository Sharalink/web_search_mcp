# AI 使用规则 - MCP 工具最佳实践

> **作者：** Emink  
> **基于：** Fábio Ferreira 的 Interactive Feedback MCP  
> **用途：** 增强版 MCP 服务器使用指南

## 🎯 核心原则

### 1. 数据优先策略
**在回答问题前，先收集相关数据**
- 使用 `web_search` 搜索最新信息
- 使用 `web_unlocker` 提取详细内容
- 使用 `create_dataset` 保存数据供后续分析

### 2. 效率优化
**批量操作 > 单个操作**
- 优先使用 `batch_url_extract` 而不是多次 `web_unlocker`
- 一次性创建完整数据集，而不是逐条添加

### 3. 自动化工作流
**减少人工干预，提高处理效率**
- 只在真正需要用户决策时使用 `interactive_feedback`
- 数据收集和分析过程应该是自动化的

## 🔄 典型工作流程

### 研究型任务
```
1. web_search → 找到相关资源
2. batch_url_extract → 批量提取内容
3. create_dataset → 保存结构化数据
4. query_dataset → 分析和总结
5. (可选) interactive_feedback → 询问用户需要深入哪些方面
```

### 数据收集任务
```
1. web_search → 找到目标网站
2. browser_automation → 执行复杂交互
3. create_dataset → 保存收集的数据
4. 直接提供结果，无需交互反馈
```

### 内容分析任务
```
1. web_unlocker → 提取文章内容
2. 直接分析和总结
3. (可选) create_dataset → 保存分析结果
```

## 📋 具体使用指南

### 🔍 Web Search 使用时机
- **总是第一步使用** - 获取最新、最相关的信息
- **设置 extract_content=true** - 当需要详细内容时
- **适当设置 num_results** - 根据任务需求调整数量

#### 示例场景
```
用户: "帮我研究一下最新的AI技术趋势"

正确做法:
1. web_search(query="2024 AI技术趋势", num_results=10, extract_content=true)
2. 分析提取的内容
3. create_dataset 保存关键信息
4. 提供综合分析结果
```

### 🔓 Web Unlocker 使用策略
- **已知URL时使用** - 当用户提供具体链接
- **需要深度内容时使用** - 当搜索结果不够详细
- **考虑使用 batch_url_extract** - 处理多个URL时

### 🤖 Browser Automation 使用场景
- **需要用户交互的网站** - 登录、表单填写
- **动态内容加载** - JavaScript渲染的页面
- **复杂操作序列** - 多步骤的网站操作

#### 高级操作示例
```json
{
  "url": "https://example.com",
  "actions": [
    {"type": "input", "selector": "#search", "text": "查询内容"},
    {"type": "click", "selector": "#submit"},
    {"type": "wait", "seconds": 3},
    {"type": "extract_text", "selector": ".results"},
    {"type": "screenshot", "path": "results.png"}
  ]
}
```

### 📊 Dataset 管理最佳实践
- **及时保存数据** - 爬取后立即创建数据集
- **结构化数据** - 使用一致的字段名称
- **合理命名** - 使用描述性的数据集名称

#### 数据结构示例
```json
[
  {
    "source_url": "https://example.com/article1",
    "title": "文章标题",
    "content": "文章内容摘要",
    "published_date": "2024-01-01",
    "category": "技术",
    "extracted_time": "2024-01-15T10:00:00Z"
  }
]
```

## ⚠️ 注意事项

### 避免过度交互
- **不要每个步骤都询问用户** - 自动完成数据收集
- **批量处理优于逐个处理** - 提高效率
- **只在关键决策点询问** - 比如选择深入分析的方向

### 错误处理
- **网络请求失败时有备选方案** - 尝试其他搜索词或网站
- **数据提取失败时提供说明** - 告知用户哪些网站无法访问
- **保存部分成功的结果** - 即使部分失败也要保存可用数据

### 性能优化
- **合理设置延迟** - 避免被网站封禁
- **限制并发请求** - 使用批量操作而非并发
- **缓存已获取的数据** - 避免重复请求相同内容

## 🎯 推荐的AI Prompt Rules

添加到您的Cursor设置中：

```
## MCP工具使用规则

1. **数据优先**: 在回答需要最新信息的问题时，始终先使用web_search收集数据
2. **批量操作**: 处理多个URL时使用batch_url_extract而不是多次web_unlocker
3. **自动化流程**: 数据收集和处理应该自动完成，只在需要用户决策时使用interactive_feedback
4. **结构化保存**: 重要的收集数据应该使用create_dataset保存为结构化格式
5. **效率优先**: 优先使用专业的工具组合完成任务，减少不必要的用户交互

## 典型工作流
- 研究任务: web_search → batch_url_extract → create_dataset → 分析总结
- 数据收集: browser_automation → create_dataset → 直接提供结果
- 内容分析: web_unlocker → 直接分析 → (可选)create_dataset保存结果
```

## 🚀 开始高效使用

将上述规则配置到您的AI助手中，让它能够：
- 🔍 智能搜索和收集数据
- 📊 自动化数据处理流程
- 💾 结构化保存重要信息
- 🤖 减少不必要的人工干预
- ⚡ 提供更快速、准确的结果 