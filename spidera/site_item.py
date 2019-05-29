import scrapy

class site_item(scrapy.Item):
    link_title = scrapy.Field()
    link_description = scrapy.Field()
    link_url = scrapy.Field()
    word1 = scrapy.Field()
    word2 = scrapy.Field()
    word3 = scrapy.Field()
    word4 = scrapy.Field()
    word5 = scrapy.Field()
    last_update = scrapy.Field()
    