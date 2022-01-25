# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader

class TudogostososcraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    preparation_time = scrapy.Field()
    portions = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    likes = scrapy.Field()
