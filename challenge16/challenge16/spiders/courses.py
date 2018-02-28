# -*- conding:utf-8 -*-

import scrapy
from challenge16.items import CourseItem

class CoursesSpider(scrapy.Spider):
    name = 'courses'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'

        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for course in response.xpath('//*[@id="user-repositories-list"]/ul/li'):
            item = CourseItem({
                    'name':course.xpath('.//div[1]/h3/a/text()').re_first('(\S+)'),
                    'update_time': course.xpath('.//relative-time/@datetime').extract_first()
                    })
            yield item


