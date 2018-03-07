# -*- conding:utf-8 -*-

import scrapy

class Spider(scrapy.Spider):
    name = 'shiyanlou-courses'

    def start_requests(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'

        urls = (url_tmpl.format(i) for i in range(1, 5))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for course in response.xpath('//*[@id="user-repositories-list"]/ul/li'):
            yield{
                    'name':course.xpath('.//div[1]/h3/a/text()').re_first('(\S+)'),
                    'update_time': course.xpath('.//relative-time/@datetime').extract_first()
                    }
            
