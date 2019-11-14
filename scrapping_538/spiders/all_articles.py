# -*- coding: utf-8 -*-

"""
Overview of latest/featured articles:
https://fivethirtyeight.com/features/

example:
https://fivethirtyeight.com/features/there-are-plenty-of-anti-trump-republicans-you-just-have-to-know-where-to-look/
https://fivethirtyeight.com/features/significant-digits-for-monday-sept-23-2019/
"""

import scrapy
from scrapping_538.items import Scrapping538Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import datetime
import socket


class BasicSpider(scrapy.Spider):
    name = 'all_articles'
    allowed_domains = ['fivethirtyeight.com']
    start_urls = (
        'http://fivethirtyeight.com',
                  )
    custom_settings = {"CLOSESPIDER_ITEMCOUNT": 50}

    def parse(self, response):
        next_selector_extract = response.css('.link-sectionmore::attr(href)').extract()
        print('....................................... length of array: %s' % len(next_selector_extract))
        # select only the last element
        print(next_selector_extract)
        next_selector_extract = [next_selector_extract[-1]]
        print(next_selector_extract)
        for url_next in next_selector_extract:
            print('....................................... url_next %s' % url_next)
            yield scrapy.Request(url_next)

        # iterate through articles
        article_divs = response.xpath('//*[@id="primary"]//div[contains(@id, "post")]')
        for article in article_divs:
            print('\n**********************************************')
            article_link = article.xpath('.//h2/a/@href').extract()[0]  # don't forget the "."
            print('------article link: ' + str(article_link))
            yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        il = ItemLoader(item=Scrapping538Item(), response=response)
        il.add_css('title', 'h1.article-title::text')
        il.add_css('date', 'time.datetime::text')
        il.add_css('hour', 'time.datetime::text')
        il.add_css('date_hour', 'time.datetime::text')
        il.add_css('author', '.author::text')
        il.add_css('filed_under', '.term::text')
        il.add_css('article_text', '.entry-content *::text')
        il.add_css('article_text_without_children', '.entry-content > *::text')
        il.add_css('mini_bio', '.mini-bio *::text')

        il.add_value('url', response.url)
        il.add_value('project', self.settings.get('BOT_NAME'))
        il.add_value('spider', self.name)
        il.add_value('server', socket.gethostname())
        il.add_value('date_import', datetime.datetime.now())
        il.add_value('PROCESSED', '0')

        return il.load_item()



