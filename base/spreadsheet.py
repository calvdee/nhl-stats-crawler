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
    self.spreadsheet = _build_spreadsheet(table_id)

  @property
  def rows(self):
    for cell in self.table:
      yield row

  def _build_spreadsheet(self, table_id):
    """
    Builds the spreadsheet 
    """
    # Extract the rows
    rows = sel.xpath(self.ROW_XPATH % table_id).extract()

    # Determine the column count from header row index
    col_count = int(float(rows[self.header_idx].xpath('count(*)').extract()[0]))

    # Project column vectors from the table
    columns = [rows.xpath(cell_xpath % i).extract() for i in 
      xrange(header_idx, col_count)]
  
    return filter(lambda c: len(c) != 0, columns)

        


    # row = [cells[i:i+n] for i in xrange(0, len(cells))]

    # for i in xrange(0, len(l), n):
    #     yield l[i:i+n]
