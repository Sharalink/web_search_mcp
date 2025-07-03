#!/bin/bash
# Git仓库设置脚本 - Web Search MCP
# 作者: Emink

echo "🚀 设置Web Search MCP Git仓库"
echo "================================"

# 检查是否已经是Git仓库
if [ -d ".git" ]; then
  echo "⚠️  检测到现有Git仓库"
  echo "是否要重新设置远程仓库? (y/n)"
  read -r response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "📝 移除现有远程仓库..."
    git remote remove origin 2>/dev/null || true
  else
    echo "❌ 操作取消"
    exit 1
  fi
else
  echo "📂 初始化Git仓库..."
  git init
fi

# 添加新的远程仓库
echo "🔗 添加远程仓库: https://github.com/Sharalink/web_search_mcp.git"
git remote add origin git@github.com:Sharalink/web_search_mcp.git

# 检查文件状态
echo "📋 当前文件状态:"
git status

echo ""
echo "🎯 下一步操作建议:"
echo "1. 添加文件: git add ."
echo "2. 提交更改: git commit -m \"feat: 初始化增强版MCP服务器 - 添加网络搜索、数据提取、浏览器自动化功能\""
echo "3. 推送到远程: git push -u origin main"
echo ""
echo "📝 提交信息模板:"
echo "   git commit -m \"feat: 初始化增强版MCP服务器"
echo "   "
echo "   - 基于Fábio Ferreira的Interactive Feedback MCP"
echo "   - 新增网络搜索和内容提取功能"
echo "   - 新增浏览器自动化操作"
echo "   - 新增数据集管理系统"
echo "   - 保留原有交互式反馈功能"
echo "   - 增强者: Emink\""

echo ""
echo "✅ Git仓库设置完成!"
