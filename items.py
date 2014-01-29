from scrapy.item import Item, Field

class TupleItem(Item): 
  """
  A list of tuples to write to a file.

  """
  tuples = Field()

class SummaryTables(Item):
  """
  An item class representing summary stats tables on player pages.
  """
  nhl_standard = Field()
  nhl_misc = Field()
  other_standard = Field()
  other_playoffs = Field()