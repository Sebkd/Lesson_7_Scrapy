import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from shopparsers.items import ShopparsersItem


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://avito.ru/?q={kwargs.get('search')}"]

    def parse(self, response: HtmlResponse):
        # поиск следующих страниц по поиску
        current_page = response.xpath("//span[contains(@class, 'pagination-item_active')]/text()").get()
        last_page = response.xpath("//span[contains(@class, 'pagination-item-JJq_j')]/text()").getall()[-2]
        # при необходимости полного поиска нужно закомментировать строчку ниже last_page = '3'
        last_page = '3'
        if current_page != last_page:
            next_page = self.start_urls[0] + '&p=' + str(int(current_page) + 1)
            yield response.follow(next_page, callback=self.parse)
        # собираем ссылки на продукты
        links = response.xpath("//h3[@itemprop='name']/..")
        for link in links:
            # link = OLX_URL + link  - это в случае использования getall()
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=ShopparsersItem(), response=response)
        loader.add_xpath('name', "//h1[contains(@class, 'title-info-title')]//text()")
        loader.add_xpath('cost', "//span[contains(@class, 'price-value-main')]//text()")
        loader.add_value('url', response.url)
        loader.add_xpath('images', "//div[contains(@class, 'gallery')]//@src")
        yield loader.load_item()

        # name = response.xpath("//h1[contains(@class, 'title-info-title')]//text()").get()
        # cost = response.xpath("//span[contains(@class, 'price-value-main')]//text()").getall()
        # url = response.url
        # images = response.xpath('//div[contains(@class, "gallery")]//@src').get() # только фото что на экране
        # # для реализации загрузок остальных фото, необходимо подключать selenium, передвигать на необходимо фото и
        # # сгружать ссылку по тому xpath. Глубина цикла равна len(response.xpath('//div[contains(@class, "gallery")]//@src'))
        #
        # yield ShopparsersItem(name=name, cost=cost, url=url, images=images)
