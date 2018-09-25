This is a scrapy spider to get "Stock Connect Northbound/Southbound from HKEXNEWS 滬港通及深港通持股紀錄 http://www.hkexnews.hk/mutualmarketsdw/main.htm

這是一個用Scrapy + Selenium 的爬蟲, 從港交所拿每天滬港通及深港通持股紀錄 

## Usage

After you download, please update the `CHROMEDRIVER_PATH` in the `settings.py`. 
and then you can start use
* scrapy crawl hkexnews (Get Today data)
* scrapy crawl hkexnews -o 123.json (will save the result to file 123.json in JSON format)
* scrapy crawl hkexnews -a date=20180921 (Get the data from Date 21-Sep-2018, the format is YYYYmmdd)

Due to limation from hkexnews, it only allow you download latest one year data. If you choose the day is not avaiable, the spider will simply ignore.

## Requirement 
* Scrapy
* Selenium
* ChromeDriver

## Database (Optional)

Mongo DB pipeline already implement you can uncomment below `#'hkexnews_scrapy.pipelines.MongoDBPipeline': 300,` in the settings.py

You can apply mlab or create your own mongo db instance to use.

## Setting
In the settings.py 

* MONGODB_URI # Mongodb URI
* MONGODB_DB  # Mongodb Name
* MONGODB_COLLECTION # Mongodb collection Name
* CHROMEDRIVER_PATH # Chromedriver path
* CHROME_HEADLESS  # Chromedriver headless mode or not, default is headless mode

## Todo

* No Idea now, please let me know if you want to enhance/ 暫時沒有想法，有意見請提出
