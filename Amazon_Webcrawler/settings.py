BOT_NAME = "Amazon_Webcrawler"

SPIDER_MODULES = ["Amazon_Webcrawler.spiders"]
NEWSPIDER_MODULE = "Amazon_Webcrawler.spiders"

# Don't obey robots.txt for this crawler
ROBOTSTXT_OBEY = False

# Add a realistic user agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 2

# Use the Zyte API add-on
DOWNLOADER_MIDDLEWARES = {
    "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
}

# Add your single Zyte API key here (choose ONE of the two keys you used)
ZYTE_API_KEY = "YOUR_ZYTE_API_KEY"

# Configure SSL certificates
# Add this to resolve SSL certificate issues
DOWNLOADER_CLIENT_TLS_METHOD = "TLSv1.2"

# For debugging
LOG_LEVEL = "INFO"
FEED_EXPORT_ENCODING = "utf-8"

# For saving results
FEEDS = {
    "laptops.json": {
        "format": "json",
        "encoding": "utf-8",
        "overwrite": True,
    },
}