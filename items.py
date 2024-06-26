from scrapy.item import Item, Field


class Image(Item):
    image_urls = Field()
    name = Field()
