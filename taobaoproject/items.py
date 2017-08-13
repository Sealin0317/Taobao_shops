# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ShopItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    k1 = Field()
    k2 = Field()
    title = Field()
    location = Field()
    rank = Field()
    rate = Field()
    sales = Field()
    amount = Field()

