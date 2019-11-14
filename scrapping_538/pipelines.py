# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class Scrapping538Pipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect('scraping538.db')
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        print('----------------------------------process_item()-------------------------------------')
        self.curr.execute("""INSERT INTO S_ARTICLES_538 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            item['title'],
            item['date'],
            item['hour'],
            item['date_hour'],
            item['author'],
            item['filed_under'],
            item['article_text'],
            item['article_text_without_children'],
            item['mini_bio'],
            item['url'][0],
            item['project'][0],
            item['spider'][0],
            item['server'][0],
            item['date_import'][0],
            item['PROCESSED'][0]
        ))
        self.conn.commit()
