# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import pymysql
from pymongo import MongoClient

'''class JdkongtiaoscrapyPipeline(object):
    def process_item(self, item, spider):
        return item'''

# example 2 use json
'''class JsonWritePipeline(object):
    def __init__(self):
        self.file = open('item.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item'''

# example 3 distinct
'''class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item'''


# 存储到MongoDB
class JingdongIntoMongoDBPipeline(object):
    def __init__(self):
        self.client = MongoClient('139.196.74.14', 27017)
        self.database = self.client['jingdong']
        self.db = self.database['jingdong_kongtiao_information']

    def process_item(self, item, spider):
        self.db.update({'goods_id': item['goods_id']}, dict(item), True)
        return item

    def close_spider(self, spider):
        self.client.close()


# 存储在MySQL
class JingdongIntoMySQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='139.196.74.14', port=3306, user='root', passwd='123456', db='jingdongDB',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            title = item['title']
            comment_count = item['comment_count']
            shop_url = item['shop_url']
            price = item['price']
            goods_url = item['goods_url']
            shops_id = item['shops_id']
            goods_id = int(item['goods_id'])
            #print(title, comment_count, shop_url,price)
            try:
                self.cursor.execute(
                        "insert into kongtiaoInfo(title,comment_count,shop_url,price,goods_url,shops_id,goods_id)values(%s,%s,%s,%s,%s,%s,%s)", (title,comment_count,shop_url,price,goods_url,shops_id,goods_id))

                self.conn.commit()
            except Exception as e:
                print("插入数据失败")
        except Exception as e1:
            pass

    #def close_spider(self):
    #    self.conn.close()
