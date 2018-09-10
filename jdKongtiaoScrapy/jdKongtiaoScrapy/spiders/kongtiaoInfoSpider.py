# -*- coding: utf-8 -*-
import scrapy

from jdKongtiaoScrapy.items import KongtiaoItem


class KongtiaoinfospiderSpider(scrapy.Spider):
    name = 'kongtiaoInfoSpider'
    allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    search_url1 = "https://search.jd.com/Search?keyword={key}&enc=utf-8&page={page}"
    search_url2 = "https://search.jd.com/s_new.php?keyword={key}&enc=utf-8&page={page}&s=27&scrolling=y&pos=30&tpl=1_M&show_items={goods_items}"
    shop_url = "http://mall.jd.com/index-{shop_id}.html"

    def start_requests(self):
        key = '空调'
        for num in range(1, 100):
            page1 = str(2 * num - 1)
            page2 = str(2 * num)
            yield scrapy.Request(url=self.search_url1.format(key=key, page=page1), callback=self.parse,
                                 dont_filter=True)
            yield scrapy.Request(url=self.search_url1.format(key=key, page=page1), callback=self.get_next_half,
                                 meta={'page2': page2, 'key': key}, dont_filter=True)

    def get_next_half(self, response):
        try:
            items = response.xpath('//*[@id="J_goodsList"]/ul/li/@data-sku').extract()
            key = response.meta['key']
            page2 = response.meta['page2']
            goods_item = ','.join(items)
            yield scrapy.Request(url=self.search_url2.format(key=key, page=page2, goods_items=goods_item),
                                 callback=self.next_parse, dont_filter=True)
        except Exception as e:
            print('没有数据')

    def parse(self, response):
        all_goods = response.xpath('//div[@id="J_goodsList"]/ul/li')
        for one_good in all_goods:
            item = KongtiaoItem()
            try:
                data = one_good.xpath('div/div/a/em')
                item['title'] = data.xpath('string(.)').extract()[0]  # 提取该标签所有的文字内容
                item['comment_count'] = one_good.xpath('div/div[@class="p-commit"]/strong/a/text()').extract()[0]  # 评论数
                item['goods_url'] = 'http:' + one_good.xpath('div/div[3]/a/@href').extract()[0]  # 商品链接
                item['shops_id'] = one_good.xpath('div/div[@class="p-img"]/div/@data-venid').extract()[0]  # 店铺ID
                item['shop_url'] = self.shop_url.format(shop_id=item['shops_id'])
                goods_id = one_good.xpath('@data-sku').extract()[0]
                if goods_id:
                    item['goods_id'] = goods_id
                price = one_good.xpath('div/div[@class="p-price"]/strong/i/text()').extract()
                if price:
                    item['price'] = price[0]
                # print(item)
                yield item
            except Exception as e:
                print('未取到数据')

    def next_parse(self, response):
        all_goods = response.xpath('/html/body/li')
        for one_good in all_goods:
            item = KongtiaoItem()
            try:
                data = one_good.xpath('div/div/a/em')
                item['title'] = data.xpath('string(.)').extract()[0]
                item['comment_count'] = one_good.xpath('div/div[@class="p-commit"]/strong/a/text()').extract()[0]
                item['goods_url'] = 'http:' + one_good.xpath('div/div[3]/a/@href').extract()[0]
                item['shops_id'] = one_good.xpath('div/div[@class="p-img"]/div/@data-venid').extract()[0]  # 店铺ID
                item['shop_url'] = self.shop_url.format(shop_id=item['shops_id'])
                goods_id = one_good.xpath('@data-sku').extract()[0]
                if goods_id:
                    item['goods_id'] = goods_id
                price = one_good.xpath('div/div[@class="p-price"]/strong/i/text()').extract()
                if price:
                    item['price'] = price[0]
                # print(item)
                yield item
            except Exception as e:
                print('未取到数据')
