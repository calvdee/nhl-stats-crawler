# Scrapy settings for nhl_stats_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nhl_stats_crawler'

SPIDER_MODULES = ['nhl_stats_crawler.spiders']
NEWSPIDER_MODULE = 'nhl_stats_crawler.spiders'

ITEM_PIPELINES = {
    # 'nhl_stats_crawler.pipelines.RosterPipeline': 100,
    'nhl_stats_crawler.pipelines.PlayerPipeline': 100,
}

LOG_LEVEL = 'INFO'

LOG_FILE = 'crawl.log'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'nhl_stats_crawler (+cdl.org)'
