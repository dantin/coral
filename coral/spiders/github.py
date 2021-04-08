# -*- coding: utf-8 -*-
from typing import List
import scrapy

from ..items import GithubItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']

    def start_requests(self):
        urls = [
            ('vim', 'https://github.com/vim/vim', ''),
            ('git', 'https://github.com/git/git', ''),
            ('FFmpeg', 'https://github.com/FFmpeg/FFmpeg', '/FFmpeg/FFmpeg/releases'),
        ]
        for target, url, next_page in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_release,
                meta={'tarball': target, 'next_page': next_page})

    def parse_release(self, response):
        if 'next_page' in response.meta and response.meta['next_page']:
            next_page = response.meta['next_page']
        else:
            next_page = parse_release_link(response)
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta=response.meta)

    def parse(self, response):
        links = parse_release_links(response)
        for url in links:
            if '.tar.gz' in url:
                yield GithubItem(name=response.meta['tarball'], file_urls=[response.urljoin(url)])
                break


def parse_release_link(response) -> str:
    target = '//div[@class="BorderGrid-cell"]/a[contains(@class, "Link--primary")]/@href'
    return response.xpath(target).get()


def parse_release_links(response) -> List[str]:
    target = ''.join((
        '//div[@class="release-entry"]/div/div[contains(@class, "main")]',
        '//ul/li[@class="d-inline-block mt-1 mr-2"]/a/@href'))
    return response.xpath(target).getall()
