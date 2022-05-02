import scrapy


class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.kz']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.olx.kz/d/list/q-{kwargs.get('search')}/"]

    def parse(self, response):
        print()
        pass
