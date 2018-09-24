# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HkexnewsScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ShanghaiStock(scrapy.Item):
    date = scrapy.Field()
    code = scrapy.Field()
    stock_cname = scrapy.Field()
    stock_ename = scrapy.Field()
    share_holding = scrapy.Field()
    percent = scrapy.Field()