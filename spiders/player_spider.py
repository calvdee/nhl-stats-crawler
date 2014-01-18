import string

from urlparse import urlparse
from nhl_stats_crawler.items import SpreadsheetItem
from nhl_stats_crawler.spreadsheet import Spreadsheet
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log


from scrapy.selector import Selector

class PlayerSpider(Spider):
  """
  Crawls the hocker-reference player pages to obtain basic 
  data for all players known to the site,
  """
  name            = "player-spider"
  allowed_domains = ["hockey-reference.com"]
  start_urls      = ["http://hockey-reference.com/players/%s" % (char) for char in list(string.ascii_lowercase)]
  
  def write_rows(self, rows, output):
    """
    Write the rows to a file.
    """
    prefix = "players-"
    filename = prefix + output

    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for row in rows:
            writer.writerow(row)    

  def parse(self, response):
    # Setup the selector
    sel = Selector(response)

    # Create base url for output
    base_url = "http://%s" % urlparse(response.url).netloc
    
    # Munge the html data and get player stats
    player_urls = map(lambda url: "%s/%s" % (base_url, url), sel.xpath('//table[@id="players"]//tr/td[1]/a/@href').extract())
    from_date = sel.xpath('//table[@id="players"]//tr/td[2]/text()').extract()
    to_date = sel.xpath('//table[@id="players"]//tr/td[3]/text()').extract()
    pos = sel.xpath('//table[@id="players"]//tr/td[4]/text()').extract()
    height = sel.xpath('//table[@id="players"]//tr/td[5]/text()').extract()
    weight = sel.xpath('//table[@id="players"]//tr/td[6]/text()').extract()
    birth_dates = sel.xpath('//table[@id="players"]//tr/td[7]/a/text()').extract()

    # Zip the attributes into rows of tuples
    zipped = zip(player_urls, from_date, to_date, pos, height, weight, birth_dates)

    # Yield tuples
    players = 0
    for row in zipped:
        players += 1
        item = RowItem()    
        item["row"] = row
        log.msg("Added %d players" % (players - 1), level=log.INFO)
        yield item

    # log.msg("Added %d items" % len(items), level=log.INFO)
    # yield items

class PlayerScoreSummarySpider(Spider):
  name            = "player-score-spider"
  allowed_domains = ["hockey-reference.com"]
  chars = list(string.ascii_lowercase)[0]
  start_urls      = ["http://hockey-reference.com/players/%s" % char for char in chars]
  
  def write_rows(self, rows, output):
    """
    Write the rows to a file.
    """
    prefix = "players-"
    filename = prefix + output

    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for row in rows:
            writer.writerow(row)    

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
    log.msg("building spreadsheet from %s" % response.url)
    
    sel = Selector(response)

    # Create the spreadsheet
    sheet = Spreadsheet(sel=sel, start_index=0, stop_index=21, table_id='stats_basic_nhl').spreadsheet  
    return SpreadsheetItem(spreadsheet=sheet)

  def get_stats_table(self):
    pass

  def get_misc_table(self):
    pass

  def get_other_table(self):
    pass

  def get_playoff_table(self):
    pass