# -*- coding: utf-8 -*-
import urllib.parse

import scrapy


class PubMedSpider(scrapy.Spider):
    name = 'pubmed'

    def __init__(self, term='', *args, **kwargs):
        super(PubMedSpider, self).__init__(*args, **kwargs)
        self.term = term

    def start_requests(self):
        url = 'https://pubmed.ncbi.nlm.nih.gov/'
        params = urllib.parse.quote_plus(self.term)
        yield scrapy.Request(url=f'{url}/?term={params}', callback=self.parse_list)

    def parse_list(self, response):
        for next_page in response.xpath(
                '//div[@class="docsum-content"]/a[@class="docsum-title"]/@href').getall():
            if not next_page:
                continue
            yield response.follow(next_page, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//h1[@class="heading-title"]/text()').get().strip()
        abstract = ' '.join(
            [s.strip() for s in response.xpath('//div[@id="enc-abstract"]//text()').getall()
                if s.strip()]
        )
        abstract = ' '.join(abstract.split(' ')).strip()
        authors = '; '.join(
            [s.strip() for s
                in response.xpath('//div[@class="authors-list"]/span/a/text()').getall()
                if s.strip()])
        orig_url = response.url
        link = response.xpath('//a[@class="id-link"][@data-ga-action="DOI"]/@href').get()
        yield {
            'title': title,
            'abstract': abstract,
            'url': orig_url,
            'authors': authors,
            'link': link,
        }
