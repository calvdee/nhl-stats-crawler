import csv

class CsvWriterPipeline(object):
  """
  A pipeline for writing items to a CSV file.
  """

  def __init__(self, sep="\t", filename="output"):
    """
    Open the file and prepare the csv writer.
    """
    fp = None
    try:
      # First try and append
      fp = open(filename, 'a')
    except Exception as e:
      fp = open(filename, 'wb')

    self.writer = csv.writer(fp, delimiter='\t')


  def process_item(self, item, spider):
    """
    Writes the item rows to a file.
    """
    self.writer.writerow(item["spreadsheet"])
    return item

class PlayerWriterPipeline(CsvWriterPipeline):
  def __init__(self):
    super(PlayerWriterPipeline, self).__init__(filename="players.tsv")

class SummarySpreadsheetPipeline(CsvWriterPipeline):
  def __init__(self):
    super(SummarySpreadsheetPipeline, self).__init__(filename="player-stats.tsv")

  def process_item(self, item, spider):
    """
    Writes the item columns to a file.
    """
    [self.writer.writerow(row) for row in item["rows"]]
    return item

class RosterSpreadsheetPipeline(CsvWriterPipeline):
  def __init__(self):
    super(RosterSpreadsheetPipeline, self).__init__(filename="rosters.tsv")

  def process_item(self, item, spider):
    """
    Writes the item columns to a file.
    """
    [self.writer.writerow(row) for row in item["tuples"]]
    return item


class RosterPipeline(CsvWriterPipeline):
  def __init__(self):
    super(GameLogPipeline, self).__init__(filename="rosters.tsv")

  def process_item(self, item, spider):
    """
    Writes the item columns to a file.
    """
    [self.writer.writerow(row) for row in item["rows"]]
    return item