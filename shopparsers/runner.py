from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from shopparsers import settings
# from shopparsers.spiders.avito import AvitoSpider
from shopparsers.spiders.leroymerlin import LeroymerlinSpider
from shopparsers.spiders.olx import OlxSpider

if __name__ == '__main__':  # ctrl+j main

    configure_logging()

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    runner = CrawlerRunner(settings=crawler_settings)

    search = 'перфоратор'

    # runner.crawl(AvitoSpider)
    runner.crawl(OlxSpider, search=search)
    # runner.crawl(LeroymerlinSpider, search=search)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
    # search = 'sumsung'
    # process_ = CrawlerProcess(settings=crawler_settings)
    # process_.crawl(OlxSpider, search=search)
    #
    # process_.crawl(HhruSpider)
    # process_.start()