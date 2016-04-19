# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobScraperItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    zip_code = scrapy.Field()
    city = scrapy.Field()
    contract = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    publication_date = scrapy.Field()
