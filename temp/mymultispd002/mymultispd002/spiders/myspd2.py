# -*- coding: utf-8 -*-
import scrapy


class Myspd2Spider(scrapy.Spider):
    name = 'myspd2'
    allowed_domains = ['baidu.com.cn']
    start_urls = ['http://baidu.com.cn/']

    def parse(self, response):
        pass
