# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AnimeItem(scrapy.Item):
    badge = scrapy.Field()
    badge_info = scrapy.Field()
    badge_type = scrapy.Field()
    cover = scrapy.Field()
    index_show = scrapy.Field()
    is_finish = scrapy.Field()
    link = scrapy.Field()
    media_id = scrapy.Field()
    order = scrapy.Field()
    order_type = scrapy.Field()
    score = scrapy.Field()
    season_id = scrapy.Field()
    season_type = scrapy.Field()
    subTitle = scrapy.Field()
    title = scrapy.Field()
    title_icon = scrapy.Field()
