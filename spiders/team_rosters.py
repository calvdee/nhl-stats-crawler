import string

from urlparse import urlparse
from nhl_stats_crawler.items import SpreadsheetItem
from nhl_stats_crawler.spreadsheet import Spreadsheet
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log


from scrapy.selector import Selector

def urls(base, x):
  return map(lambda url: "%s/%s" % (base, url), sel.xpath(x).extract())

def base_url(response):
  return "http://%s" % urlparse(response.url).netloc

class TeamRostersSpider(Spider):
  name            = "team-roster-spider"
  allowed_domains = ["hockey-reference.com"] 
  
  def __init__(self, *args, **kwargs):
    super(PlayerScoreSummarySpider, self).__init__(*args, **kwargs)
    self.start_urls = ["http://www.hockey-reference.com/teams/"]

  def parse(self, response):
    log.msg("parsing %s" % response.url)
    # Setup the selector
    sel = Selector(response)

    # Create base url for next page crawl
    base = base_url(response)
    
    # Create absolute urls from relative hrefs in player table entries
    team_urls = urls(base, '//table[@id="active_franchises"]//tr/td[1]/a/@href')

    # Yield requests for seasons
    for url in team_urls:
        yield Request(url=url, callback=self.parse_seasons)

  def parse_seasons(self, response):
    """
    """
    log.msg("parsing %s" % response.url)

    # Setup the selector
    sel = Selector(response)

    # Create base url for next page crawl
    base = base_url(response)
    
    # Create absolute urls to seasons
    team_urls = urls(base, '//table[@id="active_franchises"]//tr/td[1]/a/@href')

    # Yield requests for seasons
    for url in team_urls:
        yield Request(url=url, callback=self.parse_seasons)

  def get_stats_table(self):
    pass

  def get_misc_table(self):
    pass

  def get_other_table(self):
    pass

  def get_playoff_table(self):
    pass