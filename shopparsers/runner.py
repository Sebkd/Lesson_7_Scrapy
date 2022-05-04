from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from shopparsers import settings
# from shopparsers.spiders.avito import AvitoSpider
from shopparsers.spiders.avito import AvitoSpider
from shopparsers.spiders.leroymerlin import LeroymerlinSpider
from shopparsers.spiders.olx import OlxSpider

if __name__ == '__main__':  # ctrl+j main

    configure_logging()

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    search = 'перфоратор'

    runner = CrawlerRunner(settings=crawler_settings)

    runner.crawl(AvitoSpider, search=search)
    runner.crawl(OlxSpider, search=search)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
