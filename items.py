from scrapy.item import Item, Field

class RowItem(Item): 
	"""
	A generic item representing a row of data with columns.
	"""
  row = Field()

class SummaryTables(Item):
	"""
	An item class representing summary stats tables on player pages.
	"""
	nhl_standard = Field()
	nhl_misc = Field()
	other_standard = Field()
	other_playoffs = Field()