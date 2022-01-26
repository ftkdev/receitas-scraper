# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


def remove_line_breaks(value):
    return value.replace('\n','').strip()

class TudogostososcraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=MapCompose(remove_line_breaks))
    preparation_time = scrapy.Field(input_processor=MapCompose(remove_line_breaks))
    portions = scrapy.Field(input_processor=MapCompose(remove_line_breaks))
    link = scrapy.Field(input_processor=MapCompose(remove_line_breaks))
    author = scrapy.Field(input_processor=MapCompose(remove_line_breaks))
    likes = scrapy.Field(input_processor=MapCompose(remove_line_breaks))
    ingredients = scrapy.Field(input_processor=MapCompose(remove_line_breaks))
