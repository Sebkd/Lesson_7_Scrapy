import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from shopparsers.items import ShopparsersItem


class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.kz']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.olx.kz/d/list/q-{kwargs.get('search')}/"]

    def parse(self, response: HtmlResponse):
        OLX_URL = 'https://www.olx.kz'
        # links = response.xpath("//p[@data-testid='ad-price']/../../../../../@href").getall()
        # ищем ссыдку на следующую страницу по указателю стрелки
        next_page = response.xpath("//a[@data-cy='pagination-forward']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//p[@data-testid='ad-price']/../../../../..")
        for link in links:
            # link = OLX_URL + link  - это в случае использования getall()
            yield response.follow(link, callback=self.parse_ads)
        print()
        pass

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=ShopparsersItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('cost', "//div[@data-testid='ad-price-container']/h3/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('images', "//div[contains(@data-cy, 'adPhotos-swiperSlide')]//img/@src | //div[contains("
                                   "@data-cy, 'adPhotos-swiperSlide')]//img/@data-src")
        yield loader.load_item()

        # name = response.xpath("//h1/text()").get()
        # cost = response.xpath("//div[@data-testid='ad-price-container']/h3/text()").getall()
        # url = response.url
        # images = response.xpath(
        #     "//div[contains(@data-cy, 'adPhotos-swiperSlide')]//img/@src | "
        #     "//div[contains(@data-cy, 'adPhotos-swiperSlide')]//img/@data-src").getall()
        # yield ShopparsersItem(name=name, cost=cost, url=url, images=images)
