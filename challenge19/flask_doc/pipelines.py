# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis

class FlaskDocPipeline(object):
    def __init__(self):
        #self.con = redis.StrictRedis(host='127.0.0.1', db=0)
        pass

    def process_item(self, item, spider):
        url = item['url']
        text = item['text']
        print(url)
        print(text)
        return item
