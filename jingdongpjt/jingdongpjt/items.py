# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class KongtiaoItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    comment_num = scrapy.Field()


class InfoItem(scrapy.Item):
    brand = scrapy.Field()
    sales = scrapy.Field()
    product_info = scrapy.Field()


class CommentItem(scrapy.Item):
    user_name = scrapy.Field()
    content = scrapy.Field()
    created_time = scrapy.Field()
    pic_link = scrapy.Field()
