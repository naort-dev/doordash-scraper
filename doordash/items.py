# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoordashItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Item = scrapy.Field()
    Description = scrapy.Field()
    Price = scrapy.Field()
    Category = scrapy.Field()
    Menu = scrapy.Field()
    pass
