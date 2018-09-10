# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class MysqlpjtPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="10.88.20.201", user="root", passwd="root", db="test", charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        name = item["name"][0]
        key = item["keywd"][0]
        sql = """INSERT INTO mytb(title,keywd) VALUES (%s, %s)"""
        params = (name, key)
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
        except:
            self.conn.rollback()
        return item

    """def close_spider(self, spider):
        self.conn.close()"""

    def __del__(self):
        if self.conn:
            self.conn.close()
