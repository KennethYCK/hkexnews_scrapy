# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HkexnewsScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

import pymongo
class MongoDBPipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_col):
        self.mongo_db = mongo_db
        self.mongo_uri = mongo_uri
        self.mongo_col = mongo_col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGODB_URI'),
            mongo_db = crawler.settings.get('MONGODB_DB'),
            mongo_col = crawler.settings.get('MONGODB_COLLECTION')
        )
    
    def process_item(self, item, spider):
        self.db[self.mongo_col].insert_one(dict(item))
        return item

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]



    def close_spider(self,spider):
        self.client.close()