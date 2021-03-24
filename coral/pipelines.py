# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse

from scrapy.pipelines.files import FilesPipeline


class GithubPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        tarball, suffix = item['name'], os.path.basename(urlparse(request.url).path)
        return f'{tarball}-{suffix}'
