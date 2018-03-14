# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import json


class DoubanMoviePipeline(object):
    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def process_item(self, item, spider):
        url = item['url']
        name = item['name']
        summary = item['summary']
        score = item['score']
        items = json.dumps({'url':url, 'name':name, 'summary':summary, 'score':score})
        self.redis.lpush('douban_movie:items', items)
        return item
