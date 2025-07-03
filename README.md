# Web Search MCP - Enhanced MCP Server

> **增强开发：** Emink  
> **基于：** [Fábio Ferreira](https://x.com/fabiomlferreira) 的 Interactive Feedback MCP  
> **仓库：** https://github.com/Sharalink/web_search_mcp

这是一个功能全面的MCP（Model Context Protocol）服务器，提供强大的网络搜索、数据提取、浏览器自动化和交互式反馈功能。

![Enhanced MCP Server](https://github.com/Sharalink/web_search_mcp/blob/main/images/feedback.png?raw=true)

## 🌟 主要功能

- 🔍 **智能网络搜索** - DuckDuckGo搜索引擎集成
- 🔓 **网页内容解锁** - 绕过基本限制，提取清洁内容
- 🤖 **浏览器自动化** - 基于Selenium的Chrome自动化操作
- 📊 **数据集管理** - 创建、查询和管理CSV/JSON数据集
- 💬 **交互式反馈** - 人工智能协作工作流程
- ⚡ **批量处理** - 高效的批量URL处理能力

## 🚀 快速开始

### 1. 安装依赖

```bash
# 确保已安装Python 3.11+和uv
pip install uv

# 克隆仓库
git clone https://github.com/Sharalink/web_search_mcp.git
cd web_search_mcp

# 安装依赖
uv sync
```

### 2. 安装Chrome浏览器（用于自动化功能）

```bash
# macOS
brew install --cask google-chrome

# 或从 https://www.google.com/chrome/ 下载
```

### 3. 配置Cursor

将以下配置添加到 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "interactive-feedback": {
      "command": "/path/to/your/web_search_mcp/start_server.sh",
      "timeout": 30000,
      "autoApprove": ["interactive_feedback"]
    },
    "web-ai-assistant": {
      "command": "/path/to/your/web_search_mcp/start_pure_server.sh",
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

**重要：** 将 `/path/to/your/web_search_mcp` 替换为您的实际项目路径。

### 4. 重启Cursor并开始使用

## 🛠️ 可用工具

### 网络功能
- `web_search` - DuckDuckGo搜索，支持内容提取
- `web_unlocker` - 解锁网页内容，提取文本
- `batch_url_extract` - 批量处理多个URL

### 自动化功能  
- `browser_automation` - Chrome浏览器自动化操作

### 数据管理
- `create_dataset` - 创建CSV/JSON数据集
- `query_dataset` - 查询和过滤数据
- `list_datasets` - 列出所有数据集

### 交互功能
- `interactive_feedback` - 用户交互和反馈收集

## 📚 使用示例

### 智能研究
```
"帮我研究2024年AI技术发展趋势，收集相关数据并分析"
```
AI会自动：搜索信息 → 提取内容 → 保存数据 → 分析 → 询问深入方向

### 数据收集
```
"收集前20家AI公司的基本信息"
```
AI会自动：搜索公司 → 自动化收集 → 保存数据 → 提供结果

### 批量内容提取
```
"提取这些网址的内容：[URL列表]"
```
AI会使用：批量提取 → 保存内容 → 提供摘要

## 🎯 AI使用建议

为了最佳体验，建议在Cursor中添加以下规则：

```
## MCP工具使用策略

1. **数据优先**: 需要最新信息时，先用web_search收集数据
2. **批量优于单个**: 多URL处理用batch_url_extract 
3. **自动化流程**: 数据收集自动完成，关键决策时才用interactive_feedback
4. **结构化保存**: 重要数据用create_dataset保存
5. **效率优先**: 减少不必要的人工干预
```

## 🤝 贡献与致谢

**原作者：** [Fábio Ferreira](https://x.com/fabiomlferreira) - Interactive Feedback MCP核心功能  
**增强开发：** Emink - 网络自动化、搜索、数据管理等功能  

感谢原作者的优秀基础工作！

### 相关项目
- [原项目仓库](https://github.com/noopstudios/interactive-feedback-mcp)
- [dotcursorrules.com](https://dotcursorrules.com/)

## 📄 许可证

继承原项目许可证。原始Interactive Feedback MCP由Fábio Ferreira开发。

## 🔗 相关链接

- [MCP协议官方文档](https://modelcontextprotocol.io/)
- [Cursor文档](https://www.cursor.com/)
- [GitHub仓库](https://github.com/Sharalink/web_search_mcp)

---

**开始体验强大的AI辅助研究和数据处理能力！** 🚀