# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Compose


def fix_price(list_cost):
    try:
        for index, el in enumerate(list_cost):
            list_cost[index] = el.replace(u'\xa0', '').replace(' ', '').replace('\n', '')
        result = int(list_cost[0])
        if len(list_cost) > 2 and list_cost[1] != ' ' and list_cost is None:
            result_2 = int(list_cost[1])
            return [result, result_2, list_cost[-1]]
        return [result, list_cost[-1]]
    except:
        return list_cost


class ShopparsersItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    cost = scrapy.Field(input_processor=Compose(fix_price))
    clear_cost = scrapy.Field()
    currency = scrapy.Field()
    images = scrapy.Field()
    _id = scrapy.Field()
