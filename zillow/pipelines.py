# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ZillowPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.images_urls_field, [])
        return [Request(u, meta={"id": item.get("img_id")}) for u in urls]

    def file_path(self, request, response=None, info=None, *, item=None):
        filename = request.meta["id"]
        return f"full/{filename}.png"
