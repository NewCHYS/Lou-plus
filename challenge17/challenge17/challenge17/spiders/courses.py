# -*- conding:utf-8 -*-

import scrapy
from challenge17.items import CourseItem

class CoursesSpider(scrapy.Spider):
    name = 'courses'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'

        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for course in response.xpath('//*[@id="user-repositories-list"]/ul/li'):
            item = CourseItem()
            item['name'] = course.xpath('.//div[1]/h3/a/text()').re_first('(\S+)')
            item['update_time'] = course.xpath('.//relative-time/@datetime').extract_first()
            courses_url = response.urljoin(course.xpath('.//div[1]/h3/a/@href').extract_first())
            request = scrapy.Request(courses_url, callback=self.parse_3)
            request.meta['item'] = item
            yield request

    def parse_3(self, response):
        item = response.meta['item']

        item['commits'] = int(response.xpath('//ul[@class="numbers-summary"]/li[1]/a/span/text()').re_first('(\S+)').replace(',', ''))
        item['branches'] = int(response.xpath('//ul[@class="numbers-summary"]/li[2]/a/span/text()').re_first('(\S+)').replace(',', ''))
        item['releases'] = int(response.xpath('//ul[@class="numbers-summary"]/li[3]/a/span/text()').re_first('(\S+)').replace(',', ''))
        yield item

