# Cursor 用户规则 - MCP 工具使用策略

> **作者：** Emink  
> **用途：** Cursor全局用户规则配置  
> **基于：** Enhanced MCP Server (Web Search MCP)

## 🎯 将以下内容添加到 Cursor 的用户规则中

### 方法一：通过 Cursor 设置界面
1. 打开 Cursor
2. 进入 `Settings` → `General` → `Rules for AI`
3. 在用户规则区域添加以下内容

### 方法二：直接编辑配置文件
在 `~/.cursor/settings.json` 的 `"rules"` 部分添加以下规则

---

## 📋 用户规则内容

```
## MCP工具使用策略

### 核心原则
1. **数据优先**: 回答需要最新信息的问题时，始终先使用web_search收集数据
2. **批量操作**: 处理多个URL时使用batch_url_extract而不是多次web_unlocker  
3. **自动化流程**: 数据收集和处理应该自动完成，只在真正需要用户决策时使用interactive_feedback
4. **结构化保存**: 重要的收集数据应该使用create_dataset保存为结构化格式
5. **效率优先**: 优先使用专业的工具组合完成任务，减少不必要的用户交互

### 典型工作流程

#### 研究型任务
- 流程: web_search → batch_url_extract → create_dataset → 分析总结 → (可选)interactive_feedback
- 示例: "研究AI技术趋势" → 先搜索 → 批量提取内容 → 保存数据 → 分析 → 询问是否需要深入特定方向

#### 数据收集任务  
- 流程: web_search → browser_automation → create_dataset → 直接提供结果
- 示例: "收集公司信息" → 搜索目标 → 自动化收集 → 保存数据 → 直接展示结果

#### 内容分析任务
- 流程: web_unlocker/batch_url_extract → 直接分析 → (可选)create_dataset保存结果
- 示例: "分析这些网页" → 批量提取内容 → 分析 → 可选保存分析结果

### 工具选择指南

- **已知具体URL** → 使用 `web_unlocker` 或 `batch_url_extract`
- **需要搜索信息** → 使用 `web_search`，通常设置 `extract_content=true`
- **需要复杂网站交互** → 使用 `browser_automation`
- **需要保存数据** → 使用 `create_dataset`，优先CSV格式
- **需要查询已有数据** → 使用 `query_dataset`
- **需要用户决策** → 使用 `interactive_feedback`

### 重要注意事项

1. **避免过度交互**: 不要每个步骤都使用interactive_feedback，只在关键决策点使用
2. **批量优于逐个**: 多个URL处理时，使用batch_url_extract而不是循环调用web_unlocker
3. **数据结构化**: 收集的数据应该立即使用create_dataset保存为结构化格式
4. **错误容忍**: 网络请求失败时提供替代方案，保存部分成功的结果

### 交互式反馈使用规则
- Whenever you want to ask a question, always call the MCP interactive_feedback
- Whenever you're about to complete a user request, call the MCP interactive_feedback instead of simply ending the process
- If the feedback is empty you can end the request and don't call the mcp in loop

### 数据集管理标准

创建数据集时使用一致的结构：
```json
[
  {
    "source_url": "来源URL", 
    "title": "标题",
    "content": "内容",
    "extracted_time": "提取时间",
    "category": "分类"
  }
]
```
```

---

## 🔧 具体配置步骤

### 步骤 1: 打开Cursor设置
1. 打开Cursor
2. 使用快捷键 `Cmd/Ctrl + ,` 打开设置
3. 找到 `Rules for AI` 部分

### 步骤 2: 添加用户规则
将上面的规则内容复制粘贴到 **User Rules** 区域（不是Project Rules）

### 步骤 3: 保存并测试
1. 保存设置
2. 重启Cursor（建议）
3. 测试MCP工具功能

## ✅ 验证配置

配置完成后，您可以测试：

```
"帮我研究最新的AI工具，收集相关信息并保存数据"
```

AI应该会：
1. 自动使用web_search搜索
2. 使用batch_url_extract提取内容  
3. 使用create_dataset保存数据
4. 提供分析结果
5. 最后使用interactive_feedback询问是否需要深入研究

## 🎯 预期效果

设置这些用户规则后，您的AI助手将：
- 🔍 优先使用网络搜索获取最新信息
- ⚡ 自动化数据收集和处理流程
- 📊 结构化保存重要数据
- 💬 只在关键时刻寻求用户反馈
- 🚀 提供更高效、专业的服务体验 