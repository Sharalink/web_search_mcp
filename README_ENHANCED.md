# 增强版 MCP 服务器 (Enhanced MCP Server)

> **作者：** Emink  
> **基于：** Fábio Ferreira 的 Interactive Feedback MCP  
> **用途：** 增强版 MCP 服务器使用指南

## 🌟 概述

这是一个功能全面的MCP（Model Context Protocol）服务器，包括以下功能：

- 🔓 **Web Unlocker** - 网页内容解锁和提取
- 🔍 **Search/SERP** - 搜索引擎结果抓取  
- 🤖 **Browser Automation** - 浏览器自动化操作
- 📊 **Datasets** - 数据集管理和查询
- 💬 **Interactive Feedback** - 交互式用户反馈

## 🚀 功能特性

### 1. Web Unlocker（网页解锁器） 
- 绕过基本的网页访问限制
- 提取清洁的文本内容
- 智能重试机制
- 支持多种User-Agent策略

### 2. Search/SERP（搜索功能）
- 使用DuckDuckGo进行网络搜索
- 可选择提取搜索结果页面内容
- 支持自定义结果数量
- 返回结构化的搜索数据

### 3. Browser Automation（浏览器自动化）
- 基于Selenium的Chrome浏览器自动化
- 支持点击、输入、滚动等操作
- 可执行截屏功能
- 支持无头模式运行

### 4. Datasets（数据集管理）
- 创建和管理CSV/JSON数据集
- 数据查询和过滤功能
- 列出所有可用数据集
- 支持大量数据处理

### 5. Interactive Feedback（交互式反馈）
- 保留原有的用户交互功能
- 命令行工具集成
- 实时反馈收集

## 📦 安装配置

### 1. 安装依赖

```bash
# 确保已安装Python 3.11+和uv
pip install uv

# 安装项目依赖
uv sync
```

### 2. 安装Chrome浏览器（用于浏览器自动化）

macOS:
```bash
brew install --cask google-chrome
```

或从[Chrome官网](https://www.google.com/chrome/)下载安装

### 3. 配置Cursor

将以下配置添加到您的Cursor MCP配置文件中（通常在`~/.cursor/mcp.json`）：

```json
{
  "mcpServers": {
    "enhanced-mcp-server": {
      "command": "/path/to/your/web_search_mcp/start_enhanced_server.sh",
      "timeout": 60000,
      "autoApprove": [
        "interactive_feedback",
        "web_unlocker", 
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

**注意：** 请将 `/path/to/your/web_search_mcp/` 替换为您的实际项目路径。

## 🛠️ 使用方法

### Web Unlocker 示例
```
使用web_unlocker工具提取https://example.com的内容
```

### 搜索示例
```
使用web_search搜索"Python MCP服务器"，返回5个结果并提取内容
```

### 浏览器自动化示例
```
使用browser_automation打开Google首页，搜索"MCP协议"
Actions: [
  {"type": "input", "selector": "input[name='q']", "text": "MCP协议"},
  {"type": "click", "selector": "input[value='Google 搜索']"},
  {"type": "wait", "seconds": 3}
]
```

### 数据集管理示例
```
# 创建数据集
使用create_dataset创建名为"test_data"的CSV数据集

# 查询数据集
使用query_dataset查询"test_data.csv"中包含"example"的记录
```

## 🔧 高级配置

### 自定义User-Agent
服务器会自动使用随机User-Agent，但您可以在代码中修改`CONFIG`字典来自定义设置。

### 数据集存储
数据集默认存储在项目目录下的`datasets/`文件夹中。

### 超时设置
默认超时为30秒，可以通过修改`CONFIG["default_timeout"]`来调整。

## 🐛 故障排除

### 常见问题

1. **Chrome浏览器未找到**
   - 确保已安装Chrome浏览器
   - 检查Selenium和Chrome版本兼容性

2. **网络访问问题**
   - 某些网站可能需要更复杂的绕过策略
   - 建议使用代理或VPN

3. **权限问题**
   - 确保启动脚本有执行权限：`chmod +x start_enhanced_server.sh`

4. **依赖安装失败**
   - 尝试使用：`uv sync --reinstall`

## 📈 性能优化

- 对于大量数据处理，建议增加系统内存
- 浏览器自动化建议使用无头模式以提高性能
- 网络请求支持重试机制，可根据需要调整重试次数

## 🤝 贡献

这个项目基于 [Fábio Ferreira](https://x.com/fabiomlferreira) 的 Interactive Feedback MCP 进行增强开发。

**原作者：** [Fábio Ferreira](https://x.com/fabiomlferreira) - Interactive Feedback MCP 核心功能  
**增强开发：** Emink - Web自动化、搜索、数据集管理等扩展功能

感谢原作者的优秀基础工作！

相关项目：[dotcursorrules.com](https://dotcursorrules.com/)

## 📄 许可证

继承原项目许可证。原始 Interactive Feedback MCP 由 Fábio Ferreira 开发。

## 🔗 相关链接

- [MCP协议官方文档](https://modelcontextprotocol.io/)
- [Cursor文档](https://www.cursor.com/)
- [原项目仓库](https://github.com/noopstudios/interactive-feedback-mcp)
- [当前项目仓库](https://github.com/Sharalink/web_search_mcp)

---

**提示：** 使用本服务器时请遵守相关网站的robots.txt和使用条款。 