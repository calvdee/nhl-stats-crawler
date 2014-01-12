import csv

class CsvWriterPipeline(object):
  """
  A pipeline for writing items to a CSV file.
  """

  def __init__(self, sep="\t", ext=".tsv", filename="output"):
    """
    Open the file and prepare the csv writer.
    """
    fp = open(filename + ext, 'wb')
    self.writer = csv.writer(fp, delimiter='\t')


  def process_item(self, item, spider):
    """
    Writes the item columns to a file.
    """
    self.writer.writerow(item["row"])
    return item

class PlayerWriterPipeline(CsvWriterPipeline):
  def __init__(self):
    super(PlayerWriterPipeline, self).__init__(filename="players")