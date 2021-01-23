# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkItem(scrapy.Item):
    name = scrapy.Field()
    links = scrapy.Field()

class TextItem(scrapy.Item):
    link = scrapy.Field()
    text = scrapy.Field()

class WordItem(scrapy.Item):
    word = scrapy.Field()
    pos = scrapy.Field()
