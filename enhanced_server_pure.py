#!/usr/bin/env python3
"""
Enhanced MCP Server with web automation, search, datasets and interactive feedback capabilities.

Original Interactive Feedback MCP by Fábio Ferreira (https://x.com/fabiomlferreira)
Enhanced with web automation, search and dataset features by Emink

This module provides a comprehensive MCP server that includes:
- Web content unlocking and extraction
- Search engine results processing
- Browser automation via Selenium
- Dataset management and querying
- Interactive user feedback capabilities
"""

import asyncio
import os
import sys
import json
import re
import csv
import sqlite3
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse
import time
import random

# Core MCP imports
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Web and automation imports
import aiohttp
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import numpy as np

# Browser automation imports (optional)
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Create the server instance
server = Server("Pure Enhanced MCP Server")

# Global configuration
CONFIG = {
    "user_agent": UserAgent(),
    "default_timeout": 30,
    "max_retries": 3,
    "datasets_dir": os.path.join(os.path.dirname(__file__), "datasets"),
}

# Ensure datasets directory exists
os.makedirs(CONFIG["datasets_dir"], exist_ok=True)


# === WEB UNLOCKER FUNCTIONS ===


async def get_with_retries(
    url: str, headers: Dict[str, str] = None, proxies: Dict[str, str] = None
) -> str:
    """Get web content with retries and different strategies"""

    if headers is None:
        headers = {
            "User-Agent": CONFIG["user_agent"].random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

    strategies = [
        # Strategy 1: Direct request
        lambda: requests.get(url, headers=headers, timeout=CONFIG["default_timeout"]),
        # Strategy 2: With different user agent
        lambda: requests.get(
            url,
            headers={**headers, "User-Agent": CONFIG["user_agent"].random},
            timeout=CONFIG["default_timeout"],
        ),
        # Strategy 3: With session
        lambda: requests.Session().get(
            url, headers=headers, timeout=CONFIG["default_timeout"]
        ),
    ]

    for i, strategy in enumerate(strategies):
        try:
            await asyncio.sleep(random.uniform(0.5, 2))  # Random delay
            response = strategy()
            response.raise_for_status()
            return response.text
        except Exception as e:
            if i == len(strategies) - 1:
                raise Exception(f"All strategies failed. Last error: {str(e)}")
            continue

    raise Exception("Failed to fetch content")


async def unlock_web_content(
    url: str, extract_text: bool = True, bypass_cloudflare: bool = False
) -> Dict[str, Any]:
    """Unlock and extract content from web pages with improved content extraction"""

    try:
        content = await get_with_retries(url)
        soup = BeautifulSoup(content, "html.parser")

        # Remove unwanted elements
        for script in soup(
            ["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]
        ):
            script.decompose()

        result = {
            "url": url,
            "title": (
                soup.title.string.strip()
                if soup.title and soup.title.string
                else "No title"
            ),
            "raw_html": content if not extract_text else None,
            "status": "success",
        }

        if extract_text:
            # Try multiple strategies to extract main content
            main_content = None
            content_text = ""

            # Strategy 1: Look for common content containers
            content_selectors = [
                "main",
                "article",
                "[role='main']",
                ".content",
                ".main-content",
                ".post-content",
                ".entry-content",
                ".article-content",
                ".page-content",
                "#content",
                "#main",
                ".container .row .col",  # Bootstrap-style layout
            ]

            for selector in content_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            # Strategy 2: Find largest text block if no semantic container found
            if not main_content:
                text_divs = soup.find_all("div")
                if text_divs:
                    # Find div with most text content
                    max_text_length = 0
                    for div in text_divs:
                        div_text = div.get_text(strip=True)
                        if len(div_text) > max_text_length:
                            max_text_length = len(div_text)
                            main_content = div

            # Strategy 3: Use body as fallback
            if not main_content:
                main_content = soup.find("body") or soup

            if main_content:
                # Clean up the content
                content_text = main_content.get_text(separator=" ", strip=True)

                # Clean up excessive whitespace
                import re

                content_text = re.sub(r"\s+", " ", content_text)
                content_text = re.sub(r"\n\s*\n", "\n\n", content_text)

                result["content"] = content_text.strip()
            else:
                result["content"] = "No content could be extracted"

            # Extract metadata with improved parsing
            result["meta"] = {
                "description": "",
                "keywords": "",
                "author": "",
                "published_date": "",
                "article_length": len(content_text),
            }

            # Meta description
            meta_desc = (
                soup.find("meta", attrs={"name": "description"})
                or soup.find("meta", attrs={"property": "og:description"})
                or soup.find("meta", attrs={"name": "twitter:description"})
            )
            if meta_desc:
                result["meta"]["description"] = meta_desc.get("content", "").strip()

            # Meta keywords
            meta_keywords = soup.find("meta", attrs={"name": "keywords"})
            if meta_keywords:
                result["meta"]["keywords"] = meta_keywords.get("content", "").strip()

            # Author information
            author_selectors = [
                'meta[name="author"]',
                'meta[name="article:author"]',
                'meta[property="article:author"]',
                ".author",
                ".byline",
                ".post-author",
                '[rel="author"]',
            ]

            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    if author_elem.name == "meta":
                        result["meta"]["author"] = author_elem.get(
                            "content", ""
                        ).strip()
                    else:
                        result["meta"]["author"] = author_elem.get_text(strip=True)
                    break

            # Published date
            date_selectors = [
                'meta[property="article:published_time"]',
                'meta[name="article:published_time"]',
                'meta[name="pubdate"]',
                "time[datetime]",
                ".date",
                ".published",
                ".post-date",
            ]

            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    if date_elem.name == "meta":
                        result["meta"]["published_date"] = date_elem.get(
                            "content", ""
                        ).strip()
                    elif date_elem.name == "time":
                        result["meta"]["published_date"] = date_elem.get(
                            "datetime", ""
                        ).strip()
                    else:
                        result["meta"]["published_date"] = date_elem.get_text(
                            strip=True
                        )
                    break

        return result

    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "error": f"Content extraction failed: {str(e)}",
            "content": "",
            "title": "",
            "meta": {},
        }


# === SEARCH/SERP FUNCTIONS ===


async def search_bing(query: str, num_results: int = 10) -> List[Dict[str, str]]:
    """Search using Bing with robust parsing"""

    try:
        headers = {
            "User-Agent": CONFIG["user_agent"].random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": "https://www.bing.com/",
        }

        # Bing search URL
        search_url = "https://www.bing.com/search"
        params = {"q": query, "count": min(num_results, 50)}

        response = requests.get(
            search_url,
            headers=headers,
            params=params,
            timeout=CONFIG["default_timeout"],
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        # Try multiple parsing strategies for Bing results
        result_containers = []

        # Strategy 1: Main result containers
        result_containers.extend(soup.find_all("li", class_="b_algo"))

        # Strategy 2: Alternative result containers
        if not result_containers:
            result_containers.extend(soup.find_all("div", class_="b_algo"))

        # Strategy 3: Generic result containers
        if not result_containers:
            result_containers.extend(
                soup.find_all("div", class_=lambda x: x and "algo" in x.lower())
            )

        # Parse search results with multiple fallback strategies
        for result_div in result_containers[:num_results]:
            try:
                # Strategy 1: Standard Bing selectors
                title_link = result_div.find("h2")
                if title_link:
                    title_link = title_link.find("a")

                snippet_div = result_div.find("p") or result_div.find(
                    "div", class_="b_caption"
                )

                # Strategy 2: Alternative selectors
                if not title_link:
                    title_link = result_div.find("a", href=True)

                # Strategy 3: Generic fallbacks
                if not snippet_div:
                    snippet_div = result_div.find("span") or result_div.find("div")

                if title_link and title_link.get("href"):
                    title = title_link.get_text(strip=True)
                    url = title_link.get("href", "")
                    snippet = snippet_div.get_text(strip=True) if snippet_div else ""

                    # Clean and validate URL
                    if url.startswith("http") and not "bing.com" in url:
                        if title and len(title) > 3:  # Filter out very short titles
                            results.append(
                                {"title": title, "url": url, "snippet": snippet}
                            )

            except Exception as e:
                # Skip malformed results but continue processing
                continue

        # If no results found with main strategy, try backup extraction
        if not results:
            links = soup.find_all("a", href=True)
            for link in links[:num_results]:
                href = link.get("href", "")
                if href.startswith("http") and not any(
                    domain in href
                    for domain in ["bing.com", "microsoft.com", "msn.com"]
                ):
                    title = link.get_text(strip=True)
                    if title and len(title) > 5:  # Filter out very short titles
                        results.append({"title": title, "url": href, "snippet": ""})

        return results

    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]


async def search_and_extract(
    query: str, num_results: int = 5, extract_content: bool = False
) -> Dict[str, Any]:
    """Search and optionally extract content from results with improved error handling"""

    search_results = await search_bing(query, num_results)

    result = {
        "query": query,
        "results": search_results,
        "extracted_content": [],
        "status": "success",
    }

    if extract_content and search_results and not search_results[0].get("error"):
        # Extract content from top results with better error handling
        extraction_count = 0
        for i, search_result in enumerate(search_results):
            if extraction_count >= 3:  # Limit to 3 extractions max
                break

            if "url" in search_result and search_result["url"]:
                try:
                    content = await unlock_web_content(
                        search_result["url"], extract_text=True
                    )

                    if content.get("status") == "success":
                        # Get more content - increase from 2000 to 5000 chars
                        content_text = content.get("content", "")
                        if len(content_text) > 5000:
                            content_text = content_text[:5000] + "..."

                        result["extracted_content"].append(
                            {
                                "index": i,
                                "url": search_result["url"],
                                "title": search_result["title"],
                                "snippet": search_result.get("snippet", ""),
                                "content": content_text,
                                "meta": content.get("meta", {}),
                                "status": "success",
                            }
                        )
                        extraction_count += 1
                    else:
                        result["extracted_content"].append(
                            {
                                "index": i,
                                "url": search_result["url"],
                                "title": search_result["title"],
                                "status": "error",
                                "error": content.get(
                                    "error", "Failed to extract content"
                                ),
                            }
                        )

                except Exception as e:
                    result["extracted_content"].append(
                        {
                            "index": i,
                            "url": search_result["url"],
                            "title": search_result["title"],
                            "status": "error",
                            "error": str(e),
                        }
                    )

                # Add delay between extractions to be respectful
                await asyncio.sleep(1)

    # Add summary statistics
    result["summary"] = {
        "search_results_count": len([r for r in search_results if not r.get("error")]),
        "content_extractions_attempted": len(result["extracted_content"]),
        "content_extractions_successful": len(
            [e for e in result["extracted_content"] if e.get("status") == "success"]
        ),
    }

    return result


# === BATCH PROCESSING FUNCTIONS ===


async def batch_url_extract(
    urls: List[str], extract_text: bool = True
) -> List[Dict[str, Any]]:
    """Extract content from multiple URLs in batch"""

    results = []
    for url in urls:
        try:
            content = await unlock_web_content(url, extract_text)
            results.append(content)
            # Small delay between requests
            await asyncio.sleep(random.uniform(1, 3))
        except Exception as e:
            results.append({"url": url, "status": "error", "error": str(e)})

    return results


# === BROWSER AUTOMATION FUNCTIONS ===


def create_browser_driver(headless: bool = True) -> Optional[webdriver.Chrome]:
    """Create a Chrome WebDriver instance"""

    if not SELENIUM_AVAILABLE:
        raise Exception(
            "Selenium not available. Install selenium package for browser automation."
        )

    try:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f'--user-agent={CONFIG["user_agent"].random}')

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(CONFIG["default_timeout"])
        return driver

    except Exception as e:
        raise Exception(f"Failed to create browser driver: {str(e)}")


async def automate_browser_task(
    url: str, actions: List[Dict[str, Any]], headless: bool = True
) -> Dict[str, Any]:
    """Perform automated browser tasks"""

    if not SELENIUM_AVAILABLE:
        return {"error": "Browser automation requires Selenium package"}

    driver = None
    try:
        driver = create_browser_driver(headless=headless)
        driver.get(url)

        results = {
            "url": url,
            "actions_performed": [],
            "final_url": url,
            "page_title": "",
            "status": "success",
        }

        for action in actions:
            action_type = action.get("type", "")

            if action_type == "click":
                selector = action.get("selector", "")
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
                results["actions_performed"].append(f"Clicked: {selector}")

            elif action_type == "input":
                selector = action.get("selector", "")
                text = action.get("text", "")
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.clear()
                element.send_keys(text)
                results["actions_performed"].append(
                    f"Input text '{text}' to: {selector}"
                )

            elif action_type == "wait":
                seconds = action.get("seconds", 1)
                time.sleep(seconds)
                results["actions_performed"].append(f"Waited: {seconds} seconds")

            elif action_type == "scroll":
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                results["actions_performed"].append("Scrolled to bottom")

            elif action_type == "screenshot":
                screenshot_path = action.get("path", "screenshot.png")
                driver.save_screenshot(screenshot_path)
                results["actions_performed"].append(
                    f"Screenshot saved: {screenshot_path}"
                )

            elif action_type == "extract_text":
                selector = action.get("selector", "body")
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                extracted_text = [elem.text for elem in elements]
                results["extracted_text"] = extracted_text
                results["actions_performed"].append(f"Extracted text from: {selector}")

        results["final_url"] = driver.current_url
        results["page_title"] = driver.title

        return results

    except Exception as e:
        return {"url": url, "status": "error", "error": str(e)}
    finally:
        if driver:
            driver.quit()


# === DATASET FUNCTIONS ===


def list_datasets() -> List[Dict[str, Any]]:
    """List available datasets"""

    datasets = []
    datasets_dir = CONFIG["datasets_dir"]

    for filename in os.listdir(datasets_dir):
        filepath = os.path.join(datasets_dir, filename)
        if os.path.isfile(filepath):
            file_ext = os.path.splitext(filename)[1].lower()
            file_size = os.path.getsize(filepath)

            datasets.append(
                {
                    "name": filename,
                    "path": filepath,
                    "type": file_ext,
                    "size_bytes": file_size,
                    "size_mb": round(file_size / (1024 * 1024), 2),
                }
            )

    return datasets


def create_dataset(
    name: str, data: List[Dict[str, Any]], format_type: str = "csv"
) -> Dict[str, Any]:
    """Create a new dataset"""

    try:
        filepath = os.path.join(CONFIG["datasets_dir"], f"{name}.{format_type}")

        if format_type.lower() == "csv":
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        elif format_type.lower() == "json":
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

        return {
            "status": "success",
            "name": name,
            "path": filepath,
            "format": format_type,
            "records": len(data),
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


def query_dataset(name: str, query: str = None, limit: int = 100) -> Dict[str, Any]:
    """Query a dataset"""

    try:
        filepath = os.path.join(CONFIG["datasets_dir"], name)
        if not os.path.exists(filepath):
            return {"status": "error", "error": "Dataset not found"}

        file_ext = os.path.splitext(name)[1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(filepath)

            # Apply simple filtering if query provided
            if query:
                # Simple text search across all columns
                mask = (
                    df.astype(str)
                    .apply(lambda x: x.str.contains(query, case=False, na=False))
                    .any(axis=1)
                )
                df = df[mask]

            # Limit results
            df = df.head(limit)

            return {
                "status": "success",
                "name": name,
                "columns": df.columns.tolist(),
                "rows": len(df),
                "data": df.to_dict("records"),
            }

        elif file_ext == ".json":
            with open(filepath, "r") as f:
                data = json.load(f)

            # Simple filtering for JSON
            if query and isinstance(data, list):
                filtered_data = []
                for item in data:
                    if isinstance(item, dict):
                        if any(
                            query.lower() in str(value).lower()
                            for value in item.values()
                        ):
                            filtered_data.append(item)
                    elif query.lower() in str(item).lower():
                        filtered_data.append(item)
                data = filtered_data

            # Limit results
            if isinstance(data, list):
                data = data[:limit]

            return {"status": "success", "name": name, "type": "json", "data": data}

        else:
            return {"status": "error", "error": "Unsupported file format"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


# === MCP SERVER TOOL DEFINITIONS ===


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        # Web Unlocker
        types.Tool(
            name="web_unlocker",
            description="Unlock and extract content from web pages, bypassing basic restrictions and extracting clean text content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to unlock and extract content from",
                    },
                    "extract_text": {
                        "type": "boolean",
                        "description": "Whether to extract clean text content (default: true)",
                        "default": True,
                    },
                    "bypass_cloudflare": {
                        "type": "boolean",
                        "description": "Whether to attempt Cloudflare bypass (default: false)",
                        "default": False,
                    },
                },
                "required": ["url"],
            },
        ),
        # Batch URL Extract
        types.Tool(
            name="batch_url_extract",
            description="Extract content from multiple URLs in batch for efficient web scraping.",
            inputSchema={
                "type": "object",
                "properties": {
                    "urls": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of URLs to extract content from",
                    },
                    "extract_text": {
                        "type": "boolean",
                        "description": "Whether to extract clean text content (default: true)",
                        "default": True,
                    },
                },
                "required": ["urls"],
            },
        ),
        # Search/SERP
        types.Tool(
            name="web_search",
            description="Search the web and optionally extract content from results using Bing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of search results to return (default: 10)",
                        "default": 10,
                    },
                    "extract_content": {
                        "type": "boolean",
                        "description": "Whether to extract content from top results (default: false)",
                        "default": False,
                    },
                },
                "required": ["query"],
            },
        ),
        # Browser Automation
        types.Tool(
            name="browser_automation",
            description="Perform automated browser tasks like clicking, typing, scrolling, and extracting. Requires Chrome browser.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to navigate to",
                    },
                    "actions": {
                        "type": "array",
                        "description": "List of actions to perform",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": [
                                        "click",
                                        "input",
                                        "wait",
                                        "scroll",
                                        "screenshot",
                                        "extract_text",
                                    ],
                                    "description": "Type of action to perform",
                                },
                                "selector": {
                                    "type": "string",
                                    "description": "CSS selector for click/input/extract_text actions",
                                },
                                "text": {
                                    "type": "string",
                                    "description": "Text to input (for input actions)",
                                },
                                "seconds": {
                                    "type": "number",
                                    "description": "Seconds to wait (for wait actions)",
                                },
                                "path": {
                                    "type": "string",
                                    "description": "File path for screenshot (for screenshot actions)",
                                },
                            },
                        },
                    },
                    "headless": {
                        "type": "boolean",
                        "description": "Whether to run browser in headless mode (default: true)",
                        "default": True,
                    },
                },
                "required": ["url", "actions"],
            },
        ),
        # Dataset Management
        types.Tool(
            name="list_datasets",
            description="List all available datasets in the datasets directory.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="create_dataset",
            description="Create a new dataset from provided data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the dataset (without extension)",
                    },
                    "data": {
                        "type": "array",
                        "description": "Array of data objects/records",
                        "items": {"type": "object"},
                    },
                    "format": {
                        "type": "string",
                        "enum": ["csv", "json"],
                        "description": "Format to save the dataset (default: csv)",
                        "default": "csv",
                    },
                },
                "required": ["name", "data"],
            },
        ),
        types.Tool(
            name="query_dataset",
            description="Query and retrieve data from an existing dataset.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the dataset file (including extension)",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query to filter data (optional)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of records to return (default: 100)",
                        "default": 100,
                    },
                },
                "required": ["name"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any]
) -> list[types.TextContent]:
    """Handle tool calls"""

    try:
        if name == "web_unlocker":
            url = arguments.get("url", "")
            extract_text = arguments.get("extract_text", True)
            bypass_cloudflare = arguments.get("bypass_cloudflare", False)

            result = await unlock_web_content(url, extract_text, bypass_cloudflare)
            response = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "batch_url_extract":
            urls = arguments.get("urls", [])
            extract_text = arguments.get("extract_text", True)

            result = await batch_url_extract(urls, extract_text)
            response = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "web_search":
            query = arguments.get("query", "")
            num_results = arguments.get("num_results", 10)
            extract_content = arguments.get("extract_content", False)

            result = await search_and_extract(query, num_results, extract_content)
            response = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "browser_automation":
            url = arguments.get("url", "")
            actions = arguments.get("actions", [])
            headless = arguments.get("headless", True)

            result = await automate_browser_task(url, actions, headless)
            response = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "list_datasets":
            result = list_datasets()
            response = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "create_dataset":
            name_arg = arguments.get("name", "")
            data = arguments.get("data", [])
            format_type = arguments.get("format", "csv")

            result = create_dataset(name_arg, data, format_type)
            response = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "query_dataset":
            name_arg = arguments.get("name", "")
            query = arguments.get("query", "")
            limit = arguments.get("limit", 100)

            result = query_dataset(name_arg, query, limit)
            response = json.dumps(result, indent=2, ensure_ascii=False)

        else:
            raise ValueError(f"Unknown tool: {name}")

        return [types.TextContent(type="text", text=response)]

    except Exception as e:
        error_msg = f"Error executing {name}: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]


async def main():
    """Main entry point"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="Pure Enhanced MCP Server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
