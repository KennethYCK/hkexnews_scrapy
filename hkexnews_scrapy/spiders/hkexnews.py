# -*- coding: utf-8 -*-
import datetime
import scrapy

from hkexnews_scrapy.items import ShanghaiStock

class HkexnewsSpider(scrapy.Spider):
    name = 'hkexnews'
    allowed_domains = ['hkexnews.hk']
    start_urls = [
        'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sh',
        'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sz',
        'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk',
    ]

   
    def __init__(self, *args, **kwargs):
        self.date = kwargs.get('date', datetime.date.strftime(datetime.date.today(), "%Y%m%d"))

    def parse(self, response):
        records = response.xpath('//tr[@class="row0"] | //tr[@class="row1"]')
       
        
        for i in records:
            item = ShanghaiStock()
            result = i.xpath('td/text()').extract() 
            result = list(map(str.strip, result))
            item['code'] = result[0]
            item['stock_ename'] = result[1]
            item['share_holding'] = result[2].replace(',', '')
            item['percent'] = result[3]
            item['date'] = self.date
            
            yield item
