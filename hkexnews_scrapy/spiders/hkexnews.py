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
        self.date = kwargs.get('date', datetime.date.strftime(datetime.date.today() + datetime.timedelta(-1) , "%Y%m%d"))
        self.formdate = datetime.datetime.strptime( self.date,"%Y%m%d").strftime("%Y/%m/%d")
        self.sqldate = datetime.datetime.strptime( self.date,"%Y%m%d").strftime("%Y-%m-%d")

    def parse(self, response):
        
        formtoday = datetime.date.strftime(datetime.date.today()  , "%Y%m%d")


        return scrapy.FormRequest(
            url = response.url,
            formdata = {
                'txtShareholdingDate': self.formdate ,
                '__VIEWSTATE': response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first(),
                '__EVENTVALIDATION': response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first(),
                '__VIEWSTATEGENERATOR': response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first(),
                'btnSearch':'Search',
                'sortby':'stockcode',
                'sortDirection':'asc',
                'today': formtoday 
                },
            callback=self.after_post
        )

    def after_post(self, response):
        
        #compare the date is what we want
        html_date = response.xpath('//h2[@class="ccass-heading"]/span/text()').extract_first()
        if self.formdate in html_date:

            records = response.xpath('//*[@id="mutualmarket-result"]/tbody/tr')
            for i in records:
                item = ShanghaiStock()
                result = i.xpath('.//div/text()').extract() 
                result = list(map(str.strip, result))
                
                item['code'] = result[1]
                item['stock_ename'] = result[3]
                item['share_holding'] = result[5].replace(',', '')
                item['percent'] = result[7]
                item['date'] = self.sqldate
                
                yield item
