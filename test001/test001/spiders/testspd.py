# -*- coding: utf-8 -*-
import scrapy
from test001.items import Test001Item


class TestspdSpider(scrapy.Spider):
    name = 'testspd'
    allowed_domains = ['www.csdn.net']
    start_urls = ['https://passport.csdn.net/account/login?ref=toolbar']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
                response,
                formdata={'username': 'huoliang722@sina.com', 'password': 'H860724l'},
                callback=self.after_login
        )

    def after_login(self, response):
        item = Test001Item()
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
        item["name"] = response.xpath('/html/head/title/text()').extract()
        print(item["name"])
        return item
