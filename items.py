from scrapy.item import Item, Field

class NhlPlayer(Item):
    player = Field()
    from_year = Field()
    to_year = Field()
    pos = Field()
		height = Field()
		weight = Field()
		birth_date = Field()