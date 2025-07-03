# 🎯 最终设置指南 - 增强版MCP服务器

> **作者：** Emink  
> **基于：** Fábio Ferreira 的 Interactive Feedback MCP  
> **版本：** Enhanced MCP Server v0.1.0

## 📋 项目总览

MCP服务器生态系统，包含以下组件：

### 🔧 服务器文件
1. **`server_native.py`** - 原始交互式反馈服务器
2. **`enhanced_server.py`** - 完整功能服务器（包含交互式反馈）
3. **`enhanced_server_pure.py`** - 纯增强版服务器（专业工具集）

### 🚀 启动脚本
1. **`start_server.sh`** - 原始服务器启动脚本
2. **`start_enhanced_server.sh`** - 完整功能服务器启动脚本
3. **`start_pure_server.sh`** - 纯增强版服务器启动脚本

### ⚙️ 配置文件
1. **`cursor_config_example.json`** - 原始配置示例
2. **`cursor_config_enhanced.json`** - 单一增强版配置
3. **`cursor_config_both.json`** - 双服务器配置
4. **`cursor_config_recommended.json`** - 推荐配置（分工明确）

## 🏆 推荐配置（最佳选择）

### 配置理念
- **交互式反馈服务器** - 专门处理用户交互和反馈
- **纯增强版服务器** - 专门处理网络爬虫、搜索、数据处理等自动化任务

### 配置步骤

1. **复制推荐配置到Cursor**
   ```bash
   cp cursor_config_recommended.json ~/.cursor/mcp.json
   ```

2. **或手动编辑** `~/.cursor/mcp.json`：
   ```json
   {
     "mcpServers": {
       "interactive-feedback": {
         "command": "/Users/zch/src/dev/cursor-mcp/web_search_mcp/start_server.sh",
         "timeout": 30000,
         "autoApprove": ["interactive_feedback"]
       },
       "web-ai-assistant": {
         "command": "/Users/zch/src/dev/cursor-mcp/web_search_mcp/start_pure_server.sh",
         "timeout": 60000,
         "autoApprove": [
           "web_unlocker", 
           "batch_url_extract",
           "web_search",
           "browser_automation",
           "list_datasets",
           "create_dataset",
           "query_dataset"
         ]
       }
     }
   }
   ```

3. **重启Cursor** 以加载新配置

## 🛠️ 可用工具总览

### 交互式反馈服务器工具
- `interactive_feedback` - 用户交互和反馈收集

### Web AI助手服务器工具
- `web_unlocker` - 网页内容解锁和提取
- `batch_url_extract` - 批量URL内容提取
- `web_search` - DuckDuckGo网络搜索
- `browser_automation` - Chrome浏览器自动化
- `list_datasets` - 列出数据集
- `create_dataset` - 创建数据集
- `query_dataset` - 查询数据集

## 📚 使用场景指南

### 🔍 研究和分析
```
"请帮我研究2024年AI技术发展趋势，收集相关数据并分析"

AI会自动使用：
1. web_search - 搜索相关信息
2. batch_url_extract - 批量提取内容
3. create_dataset - 保存数据
4. 提供分析结果
5. interactive_feedback - 询问是否需要深入某些方面
```

### 📊 数据收集
```
"帮我收集前50家科技公司的基本信息"

AI会自动使用：
1. web_search - 找到公司列表
2. browser_automation - 自动化收集信息
3. create_dataset - 保存结构化数据
4. 直接提供结果（无需频繁交互）
```

### 🌐 内容提取
```
"请提取这些网址的内容：[URL列表]"

AI会使用：
1. batch_url_extract - 批量处理
2. create_dataset - 保存提取的内容
3. 提供内容摘要
```

## 🎯 AI使用规则配置

将以下规则添加到您的Cursor AI设置中：
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