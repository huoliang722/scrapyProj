# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json


class XmltestPipeline(object):
    def __init__(self):
        self.file = codecs.open(r"D:\scrapystudy\data\mydata1.json", "wb", encoding="utf-8")

    def process_item(self, item, spider):
        """l = str(item) + '\n'
        print(l)
        self.file.write(l)
        return item"""
        i = json.dumps(dict(item), ensure_ascii=False)
        line = i + '\n'
        print(line)
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
