# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from flask_doc.items import PageItem

class FlaskSpider(CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/0.12/']

    rules = (
            Rule(LinkExtractor(allow=r'http://flask.pocoo.org/docs/0.12/.*'), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        item = PageItem()
        item['url'] = response.url
        text = ' '.join(response.xpath('//text()').extract())
        item['text'] = text
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        yield item
