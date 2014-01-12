from scrapy.selector import Selector

class Table(object):
  """
  A convenience class for creating table repsresentations.
  """
  def __init__(self, sel, table_id, cols, header_idx):
    self.sel = sel
    self.table_sel = table_id
    self.cols = cols
    self.header_idx = header_idx

  @property
  def rows(self):
    for cell in self.table:
      yield row



  def _make_table(self, table_id):
    # Extract the rows
    rows = sel.xpath('//table[@id="%s"]//tr' % table_sel).extract()

    # Determine the column count from header row
    col_count = int(float(rows[self.header_idx].xpath('count(*)').extract()[0]))

    # Extract each column
    col_list = []
    for i in xrange(0, col_count):
      cols = table.xpath('td[%d]/text()' % i).extract()
      col_list.append(cols)


    # row = [cells[i:i+n] for i in xrange(0, len(cells))]

    # for i in xrange(0, len(l), n):
    #     yield l[i:i+n]