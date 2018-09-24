# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest

class SeleniumMiddleware(object):
    def __init__(self,path, option):
        
        if not option:
            
            self.driver = webdriver.Chrome(path)
            
        else:
            
            chrome_option = webdriver.ChromeOptions()
            chrome_option.add_argument('--headless')
            self.driver = webdriver.Chrome(chrome_options=chrome_option , executable_path=path)
        
        
    def process_request(self, request, spider):
        self.driver.get(request.url)
        date = spider.date #date format is 20180924
        self.driver.find_element_by_id('ddlShareholdingDay').send_keys(date[-2:])
        
        self.driver.find_element_by_id('ddlShareholdingMonth').send_keys(date[4:6])
        self.driver.find_element_by_id('ddlShareholdingYear').send_keys(date[:4])
        try:
            self.driver.find_element_by_id('btnSearch').click()
            self.driver.switch_to_alert().accept()
            
        except:
            body = self.driver.page_source
            return HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8',request = request)
        else:
            raise IgnoreRequest("not able to choose that day")
            
                   
        
    
    # @use_logging
    @classmethod
    def from_crawler(cls, crawler):
        path = crawler.settings.get('CHROMEDRIVER_PATH')
        option = crawler.settings.get('CHROME_HEADLESS')
        return cls(path, option)   

   


    def process_exception(self, request, exception, spider):
        return HtmlResponse(url=self.driver.current_url,status=404)


class HkexnewsScrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HkexnewsScrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
