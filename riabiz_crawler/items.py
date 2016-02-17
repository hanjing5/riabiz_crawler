# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RiabizCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_info_blob = scrapy.Field()
    ria_info_blob = scrapy.Field()

class RiabizDirItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    firm_name = scrapy.Field()
    directory_url = scrapy.Field()    

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()