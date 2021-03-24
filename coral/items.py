# -*- coding: utf-8 -*-
import scrapy


class GithubItem(scrapy.Item):
    name = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
