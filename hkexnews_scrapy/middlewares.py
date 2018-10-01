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
        date = spider.date #date format is 20180924
        self.driver.find_element_by_id('ddlShareholdingDay').send_keys(date[-2:])
        
        self.driver.find_element_by_id('ddlShareholdingMonth').send_keys(date[4:6])
        self.driver.find_element_by_id('ddlShareholdingYear').send_keys(date[:4])
        try:
            self.driver.find_element_by_id('btnSearch').click()
            self.driver.switch_to_alert().accept()
            
            

            
        except:
            try: #If return date not match that date we request, raise exception
                tmp_date = self.driver.find_element_by_xpath('//*[@id="pnlResult"]/div').text
                tmp_date= tmp_date.rsplit(' ',1)[1]
                tmp_date_l = tmp_date.split('/')
                tmp_date_l.reverse()
                tmp_date = "".join(tmp_date_l)
                print("temp date {}".format(tmp_date))
                if not tmp_date == date:
                    raise ValueError('Not able to choose on date')
            except:
                logger.info("Not able to choose on date %s due to no record" % date)
                raise IgnoreRequest()
            else:
                body = self.driver.page_source
                return HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8',request = request)
        else:
            logger.info("Not able to choose on date %s due to HKEX not allowed" % date)
            raise IgnoreRequest()
            
                   
        
    
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
