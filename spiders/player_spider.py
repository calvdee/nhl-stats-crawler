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
  name            = "roster-spider"
  allowed_domains = ["hockey-reference.com"] 
  
  def __init__(self, team=None, *args, **kwargs):
    super(PlayerSpider, self).__init__(*args, **kwargs)
    self.team = team
    self.start_urls = ["http://www.hockey-reference.com/teams/"]
    self.seen = set()

  def parse(self, response):
    log.msg("parsing %s" % response.url)

    # Setup the selector
    sel = Selector(response)

    # Create base url for next page crawl
    base = base_url(response)
    
    # Create absolute urls from relative hrefs in franchise table
    team_urls = urls(sel, base, '//table[@id="active_franchises"]//tr/td[1]/a/@href')


    # Process one team from command line
    if self.team != None:
        team_urls = filter(lambda url: url.rstrip('/').split('/')[-1] == self.team, 
                           team_urls)

    # Yield requests for seasons
    for url in team_urls:
        yield Request(url=url, callback=self.handle_team_url)

  def handle_team_url(self, response):
    """
    Yields Request objects to retrieve season data for a team.

    > scrapy shell http://www.hockey-reference.com/teams/ANA/

    """
    log.msg("parsing team url %s" % response.url)

    # Setup the selector
    sel = Selector(response)

    # Create base url for next page crawl
    base = base_url(response)

    # Determine table name from the URL
    table_id = response.url.rstrip('/').split('/')[-1]
    
    # Create absolute urls to seasons
    season_urls = urls(sel, base, '//table[@id="%s"]//tr/td[1]/a/@href' % table_id)

    log.msg("found %d seasons" % len(season_urls))

    # Yield urls that point to the season
    for url in season_urls:
        yield Request(url=url, callback=self.handle_season_url)

  def handle_season_url(self, response):
    """
    Generates season rosters

    > scrapy shell http://www.hockey-reference.com//teams/ANA/2014.html

    """

    log.msg("parsing game log url %s" % response.url)

    sel = Selector(response)
    
    n_players = len(sel.xpath('//table[@id="roster"]//tr/td[1]/text()'))
    year = re.sub(r'\.html', '', response.url.split('/')[-1:][0])
    team = sel.xpath('//div[@id="you_are_here"]/p/a[4]/text()').extract()[0]


    tuple_list = [
     [team for i in xrange(0, n_players)],                            # team
     [year for i in xrange(0, n_players)],                            # year
     sel.xpath('//table[@id="roster"]//tr/td[1]/text()').extract(),   # number
     sel.xpath('//table[@id="roster"]//tr/td[2]/a/text()').extract(), # player
     sel.xpath('//table[@id="roster"]//tr/td[3]/text()').extract(),   # position
     sel.xpath('//table[@id="roster"]//tr/td[4]/text()').extract(),   # age
     sel.xpath('//table[@id="roster"]//tr/td[5]/text()').extract(),   # height
     sel.xpath('//table[@id="roster"]//tr/td[6]/text()').extract(),   # weight
     sel.xpath('//table[@id="roster"]//tr/td[7]/text()').extract(),   # shoots/catches
     sel.xpath('//table[@id="roster"]//tr/td[8]/text()').extract(),   # experience
     sel.xpath('//table[@id="roster"]//tr/td[9]/text()').extract(),   # birth_date
     filter(lambda x: '-' not in x, sel.xpath('//table[@id="roster"]//tr/td[10]/text()').extract()),  # summary
    ]

    tuples = zip(*[t_list for t_list in tuple_list])

    # year_team_tuples = zip([year for i in xrange(0, len(tuple_list[0]))], tuple_list)

    return TupleItem(tuples=tuples)



    


