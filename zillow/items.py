# Define here the models for your scraped items

# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# from scrapy.loader.processors import TakeFirst
from itemloaders.processors import TakeFirst
import scrapy


class ZillowItem(scrapy.Item):

    image_urls = scrapy.Field()
    images = scrapy.Field()
    img_id = scrapy.Field(output_processor=TakeFirst())

    price = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst())
    bedroom = scrapy.Field(output_processor=TakeFirst())
    bathroom = scrapy.Field(output_processor=TakeFirst())

    area = scrapy.Field(output_processor=TakeFirst())
    type = scrapy.Field(output_processor=TakeFirst())
    details = scrapy.Field(output_processor=TakeFirst())

    broker = scrapy.Field(output_processor=TakeFirst())
    latitude = scrapy.Field(output_processor=TakeFirst())
    longitude = scrapy.Field(output_processor=TakeFirst())


