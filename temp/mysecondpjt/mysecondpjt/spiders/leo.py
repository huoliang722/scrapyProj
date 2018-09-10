# -*- coding: utf-8 -*-
import scrapy
from mysecondpjt.items import MysecondpjtItem


class LeoSpider(scrapy.Spider):
    name = 'leo'
    allowed_domains = ['sina.com.cn']
    start_urls = (
        'http://slide.news.sina.com.cn/s/slide_1_2841_103185.html#p=1',
        'http://news.sina.com.cn/pl/2016-09-12/doc-ifxvukhv8147404.shtml',
    )

    """def __init__(self, myurl=None, *args, **kwargs):
        super(LeoSpider, self).__init__(*args, **kwargs)
        # print("要爬取的网址为: %s" % myurl)
        myurllist = myurl.split("|")
        for i in myurllist:
            print("要爬取的网址为: %s" % i)
        self.start_urls = myurllist"""

    """urls2 = ("http://www.jd.com",
             "http://www.sina.com.cn",
             "http://yum.iqianyue.com",
             )

    def start_requests(self):
        for url in self.urls2:
            yield self.make_requests_from_url(url)"""

    def parse(self, response):
        item = MysecondpjtItem()
        item['urlname'] = response.xpath("/html/head/title/text()").extract()
        print(item['urlname'])
