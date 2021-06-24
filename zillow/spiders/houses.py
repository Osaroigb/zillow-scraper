from zillow.utils import URL, cookie_parser, url_parser
from scrapy.loader import ItemLoader
from zillow.items import ZillowItem
import scrapy
import json


class HousesSpider(scrapy.Spider):

    name = "houses"
    allowed_domains = ["www.zillow.com"]
    page = 1

    def start_requests(self):

        yield scrapy.Request(
            url=URL,
            headers={
                "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,es;q=0.7",
                "Cookie": cookie_parser(),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
            },
            callback=self.parse
        )

    def parse(self, response):

        resp = json.loads(s=response.body)
        cribs = resp.get("cat1").get("searchResults").get("listResults")

        for crib in cribs:

            loader = ItemLoader(item=ZillowItem())

            loader.add_value(field_name="image_urls", value=crib.get("imgSrc"))
            loader.add_value(field_name="img_id", value=crib.get("id"))

            loader.add_value(field_name="price", value=crib.get("price"))
            loader.add_value(field_name="address", value=crib.get("address"))
            loader.add_value(field_name="bedroom", value=crib.get("beds"))
            loader.add_value(field_name="bathroom", value=crib.get("baths"))

            loader.add_value(field_name="area", value=crib.get("area"))
            loader.add_value(field_name="type", value=crib.get("statusText"))
            loader.add_value(field_name="details", value=crib.get("detailUrl"))

            loader.add_value(field_name="broker", value=crib.get("brokerName"))
            loader.add_value(field_name="latitude", value=crib.get("latLong").get("latitude"))
            loader.add_value(field_name="longitude", value=crib.get("latLong").get("longitude"))

            yield loader.load_item()

        self.page += 1
        total_pages = resp.get("cat1").get("searchList").get("totalPages")

        if self.page <= total_pages:

            yield scrapy.Request(
                url=url_parser(link=URL, page_number=self.page),
                headers={
                    "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,es;q=0.7",
                    "Cookie": cookie_parser(),
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
                },
                callback=self.parse
            )
