This is a scrapy spider to get "Stock Connect Northbound/Southbound from HKEXNEWS 滬港通及深港通持股紀錄 http://www.hkexnews.hk/mutualmarketsdw/main.htm

## Usage

After you download, please update the CHROMEDRIVER_PATH = '/home/user/chromedriver/chromedriver' in the settings.py. 
and then you can start use
* scrapy crawl hkexnews_scrapy (Get Today data)
* scrapy crawl hkexnews_scrapy -o 123.json (will save the result to file 123.json)
* scrapy crawl hkexnews_scrapy -a date=20180921 (Get the data from Date 21-Sep-2018, the format is YYYYmmdd)

Due to limation from hkexnews, it only allow you download latest one year data. If you choose the day is not avaiable, the spider will simply ignore

## Requirement 
* Scrapy
* Selenium
* ChromeDriver

## Database

Mongo DB pipeline already implement you can uncomment below "#'hkexnews_scrapy.pipelines.MongoDBPipeline': 300," in the settings.py
You can apply mlab or create your own mongo db instance to 
