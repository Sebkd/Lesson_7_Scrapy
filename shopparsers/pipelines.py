# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class ShopparsersPipeline:
    def process_item(self, item, spider):
        print()
        return item


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
