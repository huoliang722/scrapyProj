# -*- coding: utf-8 -*-
import scrapy
from jingdongpjt.items import KongtiaoItem
from jingdongpjt.items import CommentItem
from jingdongpjt.items import InfoItem
import re
import urllib.request
from selenium import webdriver
import os.path
import os


class KongtiaospdSpider(scrapy.Spider):
    name = 'kongtiaospd'
    allowed_domains = ['www.jd.com/']
    start_urls = []
    for i in range(1, 5):
        url = "https://search.jd.com/Search?keyword=%E7%A9%BA%E8%B0%83&enc=utf-8&qrst=1&rt=1\
        &stop=1&vt=2&cid2=794&cid3=870&stock=1&page=" + str(2 * i - 1);
        start_urls.append(url)

    def parse(self, response):
        item = KongtiaoItem()
        # 获取标题
        item['title'] = response.xpath("//div[@class = 'p-name p-name-type-2']/a[@target='_blank']/@title").extract()
        # item['price'] = response.xpath("//div[@class='p-price']/strong/text()").extract()
        # item['name'] = response.xpath("//div[@class = 'p-name p-name-type-2']/a[@target='_blank']/em/text()").extract()
        item['link'] = response.xpath('//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()
        """print(len(item['link']))
        print(len(item['title']))
        # print(len(item['price']))
        # print(len(item['name']))"""
        for i in range(0, len(item["link"])):
            print(item['title'][i])
            print(item['link'][i])
            pattern = 'https'
            bool = re.match(pattern, item['link'][i])
            if (bool):
                continue
            else:
                file = r'D:\scrapystudy\jingdongpjt\data\product_url.txt'
                with open(file, 'a') as f:
                    f.write(item['link'][i] + '\n')
        return item



