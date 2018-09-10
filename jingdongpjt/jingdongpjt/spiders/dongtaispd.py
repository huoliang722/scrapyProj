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


class DongtaispdSpider(scrapy.Spider):
    name = 'dongtaispd'
    allowed_domains = ['jingdong.com']
    start_urls = []
    browser = webdriver.PhantomJS()
    for i in range(1, 2):
        url = "https://search.jd.com/Search?keyword=%E7%A9%BA%E8%B0%83&enc=utf-8&qrst=1&rt=1\
        &stop=1&vt=2&cid2=794&cid3=870&stock=1&page=" + str(2 * i - 1);
        start_urls.append(url)

    def parse(self, response):
        self.browser.get(self.url)
        self.browser.implicitly_wait(15)
        item = KongtiaoItem()
        unitElement = self.browser.find_element_by_id('J_goodsList')
        priceElement = unitElement.find_elements_by_xpath('./ul/li/div/div[2]/strong')
        print(len(priceElement))
        item['price'] = priceElement
        for i in range(len(item['price'])):
            print(item['price'][i].text)
