"""Source: http://doc.scrapy.org/en/1.8/topics/practices.html#run-scrapy-from-a-script
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def get_x_articles():
    process = CrawlerProcess(get_project_settings())
    # 'all_articles' is the name of one of the spiders of the project.
    process.crawl('all_articles', domain='fivethirtyeight.com')
    process.start() # the script will block here until the crawling is finished


if __name__ == "__main__":
    get_x_articles()