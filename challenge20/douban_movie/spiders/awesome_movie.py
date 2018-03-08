# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban_movie.items import MovieItem

class AwesomeMovieSpider(CrawlSpider):
    name = 'awesome-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091/']

    link = LinkExtractor(allow=r'subject/', restrict_xpaths='//*[@id="recommendations"]', process_value='lamdba x:x.replace("?form=subject-page", "")')
    rules = (
            Rule(link, callback='parse_movie_item', follow=True),
    )
    url_list = []
    def sub_url(value):
        return value.replace('?from=subject-page', '')

    def parse_movie_item(self, response):
        item = MovieItem()
        url = response.url
        score = response.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract_first()
        if url not in self.url_list and float(score) >= 8.0:
            print(url)
            self.url_list.append(url)
            item['url'] = url
            item['name'] = response.xpath('//*[@id="content"]/h1/span[1]/text()').extract_first()
            summary = response.xpath('//*[@id="link-report"]/span[@property="v:summary"]/text()').re('\S+')
            if not summary:
                summary = response.xpath('//*[@id="link-report"]/span[@class="all hidden"]/text()').re('\S+')
            print(summary)
            summary_text = ''
            for s in summary:
                summary_text += s
            item['summary'] = summary_text
            item['score'] = score
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
            return item

    def parse_start_url(self, response):
        yield self.parse_movie_item(response)

    def parse_page(self, response):
        yield self.parse_movie_item(response)
