# -*- coding: utf-8 -*-
import scrapy
from taobaopjt.items import TaobaopjtItem
from urllib.request import Request


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['ai.taobao.com']
    start_urls = ['https://detail.tmall.com/item.htm?id=523214655052&ali_refid=\
        a3_430676_1006:1102695718:N:%E7%A9%BA%E8%B0%83%E6%9F%9C%E6%9C%BA:20ccb3f9daf9b0c146c9825f8987b495&ali_trackid\
        =1_20ccb3f9daf9b0c146c9825f8987b495&spm=a231o.7712113/d.1004.272&skuId=3114957045817']

    def parse(self, response):
        urls = response.xpath('https://detail.tmall.com/item.htm?id=523214655052&ali_refid=\
        a3_430676_1006:1102695718:N:%E7%A9%BA%E8%B0%83%E6%9F%9C%E6%9C%BA:20ccb3f9daf9b0c146c9825f8987b495&ali_trackid\
        =1_20ccb3f9daf9b0c146c9825f8987b495&spm=a231o.7712113/d.1004.272&skuId=3114957045817')
        for url in urls:
            request = Request(url, callback=self.parse_post, dont_filter=True)
            request.meta['PhantomJS'] = True
            yield request

    def parse_post(self, response):
        i = TaobaopjtItem()
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        i["name"] = response.xpath('/html/head/title/text()').extract()
        print(i["name"])
        i["price"] = response.xpath('//*[@id="J_StrPriceModBox"]/dd/span/text()')
        print(i["price"])
        return i
