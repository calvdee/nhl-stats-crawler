import string

from urlparse import urlparse
from nhl_stats_crawler.items import SpreadsheetItem
# from nhl_stats_crawler.base import Spreadsheet
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log


from scrapy.selector import Selector

class Spreadsheet(object):
  """
  Creates spreadsheets from HTML tables
  """
  # :param sel The DOM selector
  # :param header_idx A row index to compute column count
  # :param table_id Id of the table element in the DOM
  # :param row_xpath A template for the table expression (defaults to xpath)
  def __init__(self, sel, header_idx, table_id, row_xpath='//table[@id="%s"]//tr'):
    self.ROW_XPATH  = row_xpath         # 
    self.CELL_XPATH = 'td[%d]/text()'
    self.sel        = sel
    self.table_id   = table_id
    self.header_idx = header_idx

    # Build the spreadsheet
    self.spreadsheet = self._build_spreadsheet(table_id)

  @property
  def columns(self):
    """
    Column generator
    """
    for col in self.spreadsheet:
      yield col

  def _build_spreadsheet(self, table_id):
    """
    Builds the spreadsheet 
    """
    # Extract the rows
    rows = self.sel.xpath(self.ROW_XPATH % table_id).extract()

    # Determine the column count from header row index
    col_count = int(float(rows[self.header_idx].xpath('count(*)').extract()[0]))

    # Project column vectors from the table
    columns = [rows.xpath(cell_xpath % i).extract() for i in 
      xrange(header_idx, col_count)]
  
    return filter(lambda c: len(c) != 0, columns)



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
    """
    @url http://www.amazon.com/s?field-keywords=selfish+gene
    @returns items 1
    @returns requests 0 0
    @scrapes SpreadsheetItem
    """
    log.msg("building spreadsheet from %s" % response.url)
    sel = Selector(response)
    ss = Spreadsheet(sel=sel, header_idx=1, table_id='stats_basic_nhl').spreadsheet
    spreadsheet = SpreadsheetItem(spreadsheet=ss)
    return spreadsheet

  def get_stats_table(self):
    pass

  def get_misc_table(self):
    pass

  def get_other_table(self):
    pass

  def get_playoff_table(self):
    pass