import csv

class PlayerWriterPipeline(object):


class CsvWriterPipeline(object):
	"""
	A pipeline for writing items to a CSV file.
	"""

	def __init__(self, sep="\t", ext=".tsv", filename="output"):
		# Overridable properties
		fp = open(filename, 'wb')
    self.writer = csv.writer(csvfile, delimiter='\t')


  def process_item(self, item, spider):
  	"""
  	Writes the item columns to a file.
  	"""
		writer.writerow(item.columns)
		return item
