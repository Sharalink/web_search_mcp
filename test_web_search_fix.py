#!/usr/bin/env python3
"""
测试Web Search工具修复效果
作者: Emink
"""

import asyncio
import json
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from enhanced_server_pure import (
    search_and_extract,
    search_duckduckgo,
    unlock_web_content,
)


async def test_search_basic():
    """测试基本搜索功能"""
    print("🔍 测试基本搜索功能...")

    query = "Python programming tutorial"
    results = await search_duckduckgo(query, num_results=5)

    print(f"搜索查询: {query}")
    print(f"结果数量: {len(results)}")

    if results and not results[0].get("error"):
        print("✅ 搜索成功!")
        for i, result in enumerate(results[:3]):
            print(f"  {i+1}. {result['title'][:50]}...")
            print(f"     URL: {result['url'][:60]}...")
            print(f"     摘要: {result['snippet'][:80]}...")
    else:
        print("❌ 搜索失败:", results[0].get("error") if results else "无结果")

    return results


async def test_search_with_extraction():
    """测试搜索+内容提取功能"""
    print("\n📄 测试搜索+内容提取功能...")

    query = "artificial intelligence 2024"
    result = await search_and_extract(query, num_results=3, extract_content=True)

    print(f"搜索查询: {query}")
    print(f"搜索结果数: {result['summary']['search_results_count']}")
    print(f"内容提取尝试: {result['summary']['content_extractions_attempted']}")
    print(f"内容提取成功: {result['summary']['content_extractions_successful']}")

    if result["extracted_content"]:
        print("✅ 内容提取成功!")
        for content in result["extracted_content"]:
            if content.get("status") == "success":
                print(f"  - {content['title'][:50]}...")
                print(f"    内容长度: {len(content['content'])} 字符")
                print(f"    内容预览: {content['content'][:100]}...")
            else:
                print(f"  - 提取失败: {content.get('error', 'Unknown error')}")
    else:
        print("❌ 内容提取失败")

    return result


async def test_content_extraction():
    """测试单独的内容提取功能"""
    print("\n🌐 测试内容提取功能...")

    # 测试一个常见的网站
    test_url = "https://www.python.org/about/"

    print(f"测试URL: {test_url}")
    result = await unlock_web_content(test_url, extract_text=True)

    if result.get("status") == "success":
        print("✅ 内容提取成功!")
        print(f"  标题: {result['title']}")
        print(f"  内容长度: {len(result.get('content', ''))} 字符")
        print(f"  作者: {result['meta'].get('author', 'N/A')}")
        print(f"  描述: {result['meta'].get('description', 'N/A')[:80]}...")
        print(f"  内容预览: {result['content'][:200]}...")
    else:
        print("❌ 内容提取失败:", result.get("error"))

    return result


async def main():
    """运行所有测试"""
    print("🧪 开始测试Web Search工具修复效果\n")

    try:
        # 测试1: 基本搜索
        await test_search_basic()

        # 测试2: 搜索+内容提取
        await test_search_with_extraction()

        # 测试3: 内容提取
        await test_content_extraction()

        print("\n🎉 测试完成!")

    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
