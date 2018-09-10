# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class JdkongtiaoscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class KongtiaoItem(Item):
    title = Field()
    comment_count = Field() #评论数
    shop_url = Field()  #店铺链接
    price = Field()
    goods_url = Field()
    shops_id = Field()
    goods_id = Field()  #商品ID


class KongtiaoInfoItem(Item):
    brand = Field()
    sales = Field()
    product_info = Field()


class KongtiaoCommentItem(Item):
    user_name = Field()
    content = Field()
    created_time = Field()
    pic_link = Field()
