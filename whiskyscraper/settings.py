"""
settings.py — Scrapy settings for the Amazon Scraper project.

Secrets (proxy credentials, Mongo URI) are loaded from environment variables.
Copy .env.example → .env and fill in your values before running.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "whiskyscraper"

SPIDER_MODULES = ["whiskyscraper.spiders"]
NEWSPIDER_MODULE = "whiskyscraper.spiders"

# ---------------------------------------------------------------------------
# Proxy & User-Agent
# ---------------------------------------------------------------------------
PROXY_USER     = os.environ.get("PROXY_USER", "")
PROXY_PASSWORD = os.environ.get("PROXY_PASSWORD", "")
PROXY_ENDPOINT = os.environ.get("PROXY_ENDPOINT", "")
PROXY_PORT     = os.environ.get("PROXY_PORT", "")

FAKEUSERAGENT_FALLBACK = "Mozilla/5.0 (Android; Mobile; rv:40.0)"

# ---------------------------------------------------------------------------
# Downloader Middlewares
# ---------------------------------------------------------------------------
DOWNLOADER_MIDDLEWARES = {
    "whiskyscraper.middlewares.MyProxyMiddleware": 350,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 400,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
}

# ---------------------------------------------------------------------------
# Crawl behaviour
# ---------------------------------------------------------------------------
ROBOTSTXT_OBEY = False

# Polite crawl delay (seconds). Uncomment to enable.
# DOWNLOAD_DELAY = 1

# ---------------------------------------------------------------------------
# Item Pipelines
# ---------------------------------------------------------------------------
ITEM_PIPELINES = {
    "whiskyscraper.pipelines.AvailabilityPipeline": 300,
    "whiskyscraper.pipelines.ProductPipeline": 400,
    "whiskyscraper.pipelines.ProductPipeline2": 401,
    "whiskyscraper.pipelines.ProductPipeline3": 402,
}