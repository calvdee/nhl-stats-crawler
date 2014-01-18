import string

from urlparse import urlparse
from nhl_stats_crawler.items import SpreadsheetItem
from nhl_stats_crawler.spreadsheet import Spreadsheet
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log


from scrapy.selector import Selector

class PlayerScoreSummarySpider(Spider):
  name            = "player-score-spider"
  allowed_domains = ["hockey-reference.com"] 
  
  def __init__(self, lastnames=None, output=None, *args, **kwargs):
    super(PlayerScoreSummarySpider, self).__init__(*args, **kwargs)
    lastnames = lastnames.split(",")
    self.start_urls = ["http://hockey-reference.com/players/%s" % char for char in lastnames]

  def parse(self, response):
    log.msg("parsing %s" % response.url)
    # Setup the selector
    sel = Selector(response)

    # Create base url for output
    base_url = "http://%s" % urlparse(response.url).netloc
    
    # Create absolute urls from relative hrefs in player table entries
    player_urls = map(lambda url: "%s/%s" % (base_url, url), sel.xpath('//table[@id="players"]//tr/td[1]/a/@href').extract())

    # Yield requests for score summary pages
    for url in player_urls:
        yield Request(url=url, callback=self.parse_summary_page)

  def parse_summary_page(self, response):
    """
    @url http://www.amazon.com/s?field-keywords=selfish+gene
    @returns items 1
    @returns requests 0 0
    @scrapes spreadsheet
    """
    sel = Selector(response)

    # Determine the player
    player_xpath = '//div[@id="info_box"]/h1/text()'
    player = sel.xpath(player_xpath).extract()[0]

    log.msg("building spreadsheet for player %s" % player)
    
    

    # Create the spreadsheet
    spreadsheet = Spreadsheet(sel=sel, 
                       start_index=0, 
                       stop_index=21, 
                       table_id='stats_basic_nhl')

    # Map the players onto the front of the rows
    rows = [[player] + row for row in spreadsheet.rows]

    return SpreadsheetItem(rows=rows)

  def get_stats_table(self):
    pass

  def get_misc_table(self):
    pass

  def get_other_table(self):
    pass

  def get_playoff_table(self):
    pass