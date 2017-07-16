# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MistoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_name = scrapy.Field()
    app_size = scrapy.Field(serializer = str)
    app_version = scrapy.Field()
    app_updatetime = scrapy.Field()
    app_package = scrapy.Field()
    app_company = scrapy.Field()
    company_tel = scrapy.Field()
    company_email = scrapy.Field()
    company_address = scrapy.Field()
    company_url = scrapy.Field()
    pass
