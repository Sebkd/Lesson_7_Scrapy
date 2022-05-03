import scrapy
from scrapy.http import HtmlResponse


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://avito.ru/?q-{kwargs.get('search')}"]


    def parse(self, response: HtmlResponse):
        print()
        pass
