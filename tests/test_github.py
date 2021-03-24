# -*- coding: utf-8 -*-
import os

import pytest
from scrapy.http import TextResponse

from coral.spiders.github import parse_release_link, parse_release_links


@pytest.fixture
def landing_page(page_path):
    with open(os.path.join(page_path, 'landing_page.html'), 'r') as f:
        return f.read()


@pytest.fixture
def release_page(page_path):
    with open(os.path.join(page_path, 'release_page.html'), 'r') as f:
        return f.read()


def test_parse_release_link(landing_page):
    response = TextResponse(
        url='https://github.com/vim/vim',
        encoding='utf-8',
        body=landing_page)
    url = parse_release_link(response)
    assert url == '/vim/vim/releases'


def test_parse_release_links(release_page):
    response = TextResponse(
        url='https://github.com/vim/vim/releases',
        encoding='utf-8',
        body=release_page)
    urls = parse_release_links(response)
    assert len(urls) > 0
