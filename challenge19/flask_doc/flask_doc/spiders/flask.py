# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from flask_doc.items import PageItem
import re

class FlaskSpider(CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/0.12/']

    rules = (
            Rule(LinkExtractor(allow=r'/#'), callback='parse_page', follow=True),
    )

    u = []

    def parse_page(self, response):
        text = ''
        url = response.url
        if url not in self.u:
            self.u.append(url)
            item = PageItem()
            item['url'] = url
            text_temp = response.xpath("//div[@class='body']").xpath('.//text()').extract()
            for t in text_temp:
                text += t
            text = re.sub('(\s\s+)', r' ', text)
            item['text'] = text
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return item
