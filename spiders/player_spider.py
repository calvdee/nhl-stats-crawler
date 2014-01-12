import string

from urlparse import urlparse
from nhl_stats_crawler.items import RowItem
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log

class PlayerSpider(Spider):
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
    
    # Munge the html data
    player_urls = map(lambda url: "%s/%s" % (base_url, url), sel.xpath('//table[@id="players"]//tr/td[1]/a/@href').extract())
    from_date = sel.xpath('//table[@id="players"]//tr/td[2]/text()').extract()
    to_date = sel.xpath('//table[@id="players"]//tr/td[3]/text()').extract()
    pos = sel.xpath('//table[@id="players"]//tr/td[4]/text()').extract()
    height = sel.xpath('//table[@id="players"]//tr/td[5]/text()').extract()
    weight = sel.xpath('//table[@id="players"]//tr/td[6]/text()').extract()
    birth_dates = sel.xpath('//table[@id="players"]//tr/td[7]/a/text()').extract()

    zipped = zip(player_urls, from_date, to_date, pos, height, weight, birth_dates)

    # Create the row by zipping columns
    items = []
    for row in zipped:
        item = RowItem()    
        item["row"] = row
        yield item

    # log.msg("Added %d items" % len(items), level=log.INFO)
    # yield items