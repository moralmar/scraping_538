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
import re
from scrapy.http import Request
from urllib.parse import urljoin


class BasicSpider(scrapy.Spider):
    name = 'one_article'
    allowed_domains = ['web']
    start_urls = (
        'https://fivethirtyeight.com/features/lebron-is-great-at-everything-even-point-guard/',
                  )

    def parse(self, response):

        l = ItemLoader(item=Scrapping538Item(), response=response)
        l.add_css('title', 'h1.article-title::text')
        l.add_css('date', 'time.datetime::text')
        l.add_css('hour', 'time.datetime::text')
        l.add_css('date_hour', 'time.datetime::text')
        l.add_css('author', '.author::text')
        l.add_css('filed_under', '.term::text')

        # xpath tests: response.xpath('//div[@class="entry-content single-post-content"]').getall()
        l.add_css('article_text', '.entry-content *::text')
        l.add_css('article_text_without_children', '.entry-content > *::text')

        l.add_css('mini_bio', '.mini-bio *::text')

        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date_import', datetime.datetime.now())
        l.add_value('PROCESSED', '0')

        return l.load_item()



