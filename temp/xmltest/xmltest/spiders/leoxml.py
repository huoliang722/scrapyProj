# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from xmltest.items import XmltestItem


class LeoxmlSpider(XMLFeedSpider):
    name = 'leoxml'
    allowed_domains = ['sina.com.cn']
    # start_urls = ['http://blog.sina.com.cn/rss/1288814951.xml']
    start_urls = (
        'http://tech.sina.com.cn/d/s/2016-09-17/doc-ifxvyqwa3324638.shtml',
        'http://sina.com.cn',
        'http://blog.sina.com.cn/rss/1288814951.xml',
    )
    iterator = 'iternodes'  # you can change this; see the docs
    itertag = 'rss'  # change it accordingly

    def parse_node(self, response, selector):
        i = XmltestItem()
        # i['url'] = selector.select('url').extract()
        # i['name'] = selector.select('name').extract()
        # i['description'] = selector.select('description').extract()
        i['title'] = selector.xpath("/rss/channel/item/title/text()").extract()
        i['link'] = selector.xpath("/rss/channel/item/link/text()").extract()
        i['author'] = selector.xpath("/rss/channel/item/author/text()").extract()
        i['category'] = selector.xpath("/rss/channel/item/category/text()").extract()
        for j in range(len(i['title'])):
            print("第 " + str(j + 1) + " 个文章 ")
            print(" 的标题是： ")
            print(i['title'][j])
            print(" 对应链接是：")
            print(i['link'][j])
            print(" 对应作者是： ")
            print(i['author'][j])
            print(" 对应目录是： ")
            print(i['category'][j])
            print("-------------------------------------")
        return i
