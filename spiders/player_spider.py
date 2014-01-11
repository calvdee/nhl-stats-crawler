import string
import csv
from urlparse import urlparse
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader

class PlayerSpider(BaseSpider):
  name            = "player-spider"
  allowed_domains = ["hockey-reference.com"]
  start_urls      = ["http://hockey-reference.com/players/%s" % (char) for char in list(string.ascii_lowercase)]
  
  def generate_rows(self, response):
    """
    Create an in-memory representation of the html table.
    """

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

    # Create the row by zipping columns
    return zip(player_urls, from_date, to_date, pos, height, weight, birth_dates)

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
    # Create the rows 
    rows = self.generate_rows(response)

    # Write the rows to the filename (alpha char)
    filename = response.url.split('/')[-2:-1][0]
    self.write_rows(rows, "%s.tsv" % filename)