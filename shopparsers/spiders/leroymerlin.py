from pprint import pprint

import scrapy
import logging


class LeroymerlinSpider(scrapy.Spider):
    # handle_httpstatus_list = [401,]
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://leroymerlin.ru/search/?q={kwargs.get('search')}&suggest=true"]

    def parse(self, response):
        print()
        # self.log("Logging in...", level=logging.INFO)
        pass
