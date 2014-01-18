from scrapy.selector import Selector

class Spreadsheet(object):
  """
  Creates spreadsheets from HTML tables
  """
  # :param sel The DOM selector
  # :param table_id Id of the table element in the DOM
  # :param start_idx The starting column index
  # :param stop_idx The (1-based) stopping column index 
  # :param row_xpath A template for the table expression (defaults to xpath)
  def __init__(self, sel, table_id, start_index=0, stop_index=0):
    assert(stop_index != None, "need stop index")
    self.sel        = sel
    self.table_id   = table_id
    self.n_cols = (stop_index - 1) - start_index

    # Build the spreadsheet
    self.rows = self._build_spreadsheet(table_id)

  @property
  def columns(self):
    """
    Column generator
    """
    for col in self.rows:
      yield col

  def _build_spreadsheet(self, table_id):
    """
    Builds the spreadsheet 
    """
    row_sel = self._rows(self.sel, self.table_id)
    rows = [self._cells(row) for row in row_sel]

    # Remove empty rows and return the rows
    return filter(lambda r: len(r) != 0, rows)

  def _rows(self, sel, table_id): 
    """ Returns table row nodes """
    return sel.xpath('//table[@id="%s"]//tr' % table_id)

  def _cells(self, sel): 
    """ Returns extracted cells """
    return sel.xpath('td/text()').extract()
    
  """ Yield successive n-sized chunks from l """
  def _chunks(self, l, n): 
    return [l[i:i+n] for i in xrange(0, len(l), n)]