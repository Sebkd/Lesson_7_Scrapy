# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import numbers

import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class ShopparsersPipeline:
    def __init__(self):
        # не забывай включить процесс mongod.service
        # systemctl start mongod.service
        # systemctl status mongod.service
        client = MongoClient('localhost', 27017)
        self.mongobase = client.shopparser

    def process_item(self, item, spider):
        item['clear_cost'], item['currency'] = self.clear_cost(item['cost'])
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def clear_cost(self, cost):
        '''
        Преобразования предварительного массива в данные. Если условия не выполняются, то в чистую цену заносится
        предварительно очищенный массив
        :param cost: предварительный массив содержащий цену, валюту
        :return: отдельно цена и отдельно валюта
        '''
        if isinstance(cost[0], numbers.Number):
            clear_cost = cost[0]
            if len(cost) > 1:
                currency = cost[-1]
            return clear_cost, currency
        return cost, '---'



class ShopImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as error:
                    print(error)

    def item_completed(self, results, item, info):
        item['images'] = [el[1] for el in results if el[0]]
        return item
