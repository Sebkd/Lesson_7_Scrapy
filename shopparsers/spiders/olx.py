import scrapy
from scrapy.http import HtmlResponse


class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.kz']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.olx.kz/d/list/q-{kwargs.get('search')}/"]

    #     //p[@data-testid='ad-price']/../../../../../@href


    def parse(self, response: HtmlResponse):
        OLX_URL = 'https://www.olx.kz'
        # links = response.xpath("//p[@data-testid='ad-price']/../../../../../@href").getall()
        links = response.xpath("//p[@data-testid='ad-price']/../../../../..")
        for link in links:
            # link = OLX_URL + link
            yield response.follow(link, callback=self.parse_ads)
        print()
        pass

    def parse_ads(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").get()
        cost = response.xpath("//div[@data-testid='ad-price-container']/h3/text()").getall()
        url = response.url
