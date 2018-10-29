# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SeleniumMiddleware(object):
    def __init__(self,path, option):
        
        if not option:
            
            self.driver = webdriver.Chrome(path)
            
        else:
            
            chrome_option = webdriver.ChromeOptions()
            chrome_option.add_argument('--headless')
            self.driver = webdriver.Chrome(chrome_options=chrome_option , executable_path=path)
        self.driver.implicitly_wait(3)
        
        
    def process_request(self, request, spider):
        self.driver.get(request.url)
        date = spider.date #date format is 2018-09-24

        input = self.driver.find_element_by_id('txtShareholdingDate')

        
        tmp = datetime.strptime( date ,"%Y-%m-%d").strftime("%Y/%m/%d")

        self.driver.execute_script('arguments[0].value="' + tmp +'";', input)
        self.driver.find_element_by_id('btnSearch').click()
        
        
        body = self.driver.page_source
        return HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8',request = request)
        
            
            
        
                   
        
    
    # @use_logging
    @classmethod
    def from_crawler(cls, crawler):
        path = crawler.settings.get('CHROMEDRIVER_PATH')
        option = crawler.settings.get('CHROME_HEADLESS')
        s = cls(path, option)   
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s 

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        self.driver.quit()
        spider.logger.info('Spider closed: %s' % spider.name)

    def process_exception(self, request, exception, spider):
        return HtmlResponse(url=self.driver.current_url, status=404)
