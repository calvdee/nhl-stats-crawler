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

class RosterPipeline(CsvWriterPipeline):
  def __init__(self):
    super(RosterPipeline, self).__init__(filename="rosters.csv")

  def process_item(self, item, spider):
    """
    Writes the roster tuples to a file.
    """
    [self.writer.writerow(tup) for tup in item["tuples"]]
    return item

class PlayerPipeline(CsvWriterPipeline):
  def __init__(self):
    super(PlayerPipeline, self).__init__(filename="players.csv")

  def process_item(self, item, spider):
    """
    Writes the roster tuples to a file.
    """
    [self.writer.writerow(tup) for tup in item["tuples"]]
    return item