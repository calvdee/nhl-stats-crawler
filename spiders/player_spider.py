import string

from urlparse import urlparse
from nhl_stats_crawler.items import RowItem
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log

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
    
    # Munge the html data to obtain players
    player_urls = map(lambda url: "%s/%s" % (base_url, url), sel.xpath('//table[@id="players"]//tr/td[1]/a/@href').extract())
    from_date = sel.xpath('//table[@id="players"]//tr/td[2]/text()').extract()
    to_date = sel.xpath('//table[@id="players"]//tr/td[3]/text()').extract()
    pos = sel.xpath('//table[@id="players"]//tr/td[4]/text()').extract()
    height = sel.xpath('//table[@id="players"]//tr/td[5]/text()').extract()
    weight = sel.xpath('//table[@id="players"]//tr/td[6]/text()').extract()
    birth_dates = sel.xpath('//table[@id="players"]//tr/td[7]/a/text()').extract()

    zipped = zip(player_urls, from_date, to_date, pos, height, weight, birth_dates)

    # Yield table rows
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
    
    # Create absolute urls from relative hrefs in player table entries
    player_urls = map(lambda url: "%s/%s" % (base_url, url), 
        sel.xpath('//table[@id="players"]//tr/td[1]/a/@href').extract())

    # Yield requests for score summary pages
    for url in player_urls:
        yield Request(url=url, callback=self.parse_summary_page)

  def parse_summary_page(self, response):
    log.msg("Visited %s" % response.url)

  def get_stats_table(self):
    pass

  def get_misc_table(self):
    pass

  def get_other_table(self):
    pass

  def get_playoff_table(self):
    pass