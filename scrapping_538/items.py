# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, Join, Compose, MapCompose

class Scrapping538Item(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
        self.log('title: %s' % response.css('h1.article-title').xpath('text()').getall()[0])
        self.log('date:  %s' % response.css('time.datetime').xpath('text()').getall()[0])
        self.log('hour:  %s' % response.css('time.datetime').xpath('text()').getall()[1])
        self.log('author:  %s' % response.css('.author').xpath('text()').getall())
        self.log('filed_under:  %s' % response.css('.term').xpath('text()').getall())
        self.log('article_text:   %s' % response.css('.entry-content').xpath('string()').getall())
        self.log('mini_bio:  %s' % response.css('.mini-bio').xpath('string()').getall())
    """
    # https://stackoverflow.com/questions/28534125/list-comprehension-elegantly-strip-and-remove-empty-elements-in-list
    def compact(s):
        return s if s else None

    # https://xbuba.com/questions/50302209
    # lambda x: x.replace('\t', '').replace('\n', '').strip()
    clean_text = Compose(Join(),
                         lambda x: x.strip()
                         )

    title = Field(output_processor=clean_text)
    date = Field(output_processor=TakeFirst())
    hour = Field(output_processor=Compose(lambda x: x[1]))
    date_hour = Field(output_processor=Join(separator='-'))
    author = Field(output_processor=TakeFirst())
    filed_under = Field(output_processor=Join(separator='-'))
    article_text = Field(output_processor=clean_text)
    article_text_without_children = Field(output_processor=clean_text)
    mini_bio = Field(output_processor=clean_text)
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date_import = Field()
    PROCESSED = Field()
    pass
