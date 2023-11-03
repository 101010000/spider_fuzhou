# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyFuzhouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    email = scrapy.Field()
    # name = scrapy.Field()
    tel = scrapy.Field()
    # web = scrapy.Field()
    pass
