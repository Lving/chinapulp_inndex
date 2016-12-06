# -*- coding: utf-8 -*-

# Scrapy settings for chinapulp_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'chinapulp_spider'

SPIDER_MODULES = ['chinapulp_spider.spiders']
NEWSPIDER_MODULE = 'chinapulp_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'chinapulp_spider (+http://www.yourdomain.com)'


COOKIES_ENABLED = False
DOWNLOAD_DELAY = 3
# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# 随机ua设置
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'chinapulp_spider.middlewares.RotateUserAgentMiddleware': 400,
}

ITEM_PIPELINES = {
    'chinapulp_spider.pipelines.ChinapulpSpiderPipeline': 300,
}
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_DB = 'test'
MYSQL_PASSWORD = 'root'







