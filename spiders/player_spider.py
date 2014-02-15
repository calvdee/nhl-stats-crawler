import re
import string
import re
from urlparse import urlparse
from nhl_stats_crawler.items import TupleItem
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from scrapy.selector import Selector


def urls(sel, base, x):
  return map(lambda url: "%s/%s" % (base, url), sel.xpath(x).extract())

def base_url(response):
  return "http://%s" % urlparse(response.url).netloc

class PlayerSpider(Spider):
  name            = "player-spider"
  allowed_domains = ["hockey-reference.com"] 
  
  def __init__(self, team=None, *args, **kwargs):
    super(PlayerSpider, self).__init__(*args, **kwargs)
    self.team = team
    self.start_urls = ["http://www.hockey-reference.com/players/%s" % c for c in string.ascii_lowercase]
    self.seen = set()

  def parse(self, response):
    """
    Yields Request objects to retrieve player data for NHL players

    > scrapy shell http://www.hockey-reference.com/players/a/

    """

    log.msg("parsing %s" % response.url)

    # Setup the selector
    sel = Selector(response)

    # Create base url for next page crawl
    base = base_url(response)
    
    # Only get NHL players and create absolute urls from relative hrefs in player table
    player_urls = urls(sel, base, '//table[@id="players"]//tr[@class="nhl"]/td[1]/a/@href')

    # Yield requests for players
    for url in player_urls:
        yield Request(url=url, callback=self.handle_player_url)

  def handle_player_url(self, response):
    """
    Yields Request objects to retrieve season data for a team.

    > scrapy shell http://www.hockey-reference.com/players/a/aaltoan01.html

    """
    log.msg("parsing player url %s" % response.url)

    # Setup the selector
    sel = Selector(response)

    # Scrape the data 
    # We slice most of the lists because the last row is used for summations
    tuple_list = [
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[1]/text()').extract()[0:-1],    # Season
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[2]/text()').extract(),          # Age
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[3]/a/text()').extract(),        # Team
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[4]/a/text()').extract()[0:-1],  # League
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[5]/text()').extract()[0:-1],    # Games Played
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[6]/text()').extract()[0:-1],    # Goals
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[7]/text()').extract()[0:-1],    # Assists
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[8]/text()').extract()[0:-1],    # Points
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[9]/text()').extract()[0:-1],    # Goals Created
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[10]/text()').extract()[0:-1],    # Plus Minus
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[11]/text()').extract()[0:-1],    # Penalties in Minutes
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[12]/text()').extract()[0:-1],    # Even Strength Goals
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[13]/text()').extract()[0:-1],    # Power Play Goals
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[14]/text()').extract()[0:-1],    # Short Handed Goals
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[15]/text()').extract()[0:-1],    # Game-Winning Goals
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[16]/text()').extract()[0:-1],    # Even Strength Assists
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[17]/text()').extract()[0:-1],    # Short-Handed Assists
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[18]/text()').extract()[0:-1],    # Power Play Assists
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[19]/text()').extract()[0:-1],    # Shots
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[20]/text()').extract()[0:-1],    # Shooting Percentage
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[21]/text()').extract()[0:-1],    # Time On Ice
     sel.xpath('//table[@id="stats_basic_nhl"]//tr/td[22]/text()').extract()[0:-1]    # Average Time On Ice
    ]

    tuples = zip(*[t_list for t_list in tuple_list])

    return TupleItem(tuples=tuples)


    


