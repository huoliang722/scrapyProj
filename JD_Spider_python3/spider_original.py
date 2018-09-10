# coding:utf-8

import requests
import re
from bs4 import BeautifulSoup
import lxml
import threading
from queue import Queue
import codecs
import json
from SQL import save_mysql  # 导入sql存储数据
import pymysql as db


class spiders:
    def __init__(self, page):
        self.url = 'https://search.jd.com/Search?keyword=空调&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V16&wq=kongt&cid2=794&cid3=870&stock=1&page=' + str(
                page)
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        self.search_urls = 'https://search.jd.com/Search?keyword=空调&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V16&wq=\
        kongt&cid2=794&cid3=870&stock=1&page={0}&s=26&scrolling=y&pos=30&show_items={1}'
        self.pids = set()  # 页面中所有的id,用来拼接剩下的30张图片的url,使用集合可以有效的去重
        self.product_urls = set()
        self.img_urls = set()  # 得到的所有图片的url
        self.search_page = page + 1  # 翻页的作用
        self.sql = save_mysql()  # 数据库保存

    # 得到每一页的网页源码
    def get_html(self):
        res = requests.get(self.url, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        return html

    # 得到每一个页面的id
    def get_pids(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        lis = soup.find_all("li", class_='gl-item')
        for l in lis:
            data_pid = l.get("data-sku")
            if (data_pid):
                self.pids.add(data_pid)
                # print self.pids
                # print "-------------------------------------------------------------"

    def get_product_url(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        lis = soup.find_all("li", class_='gl-item')
        for l in lis:
            product_url_upper = l.find('div', class_="p-name p-name-type-2")
            product_url = product_url_upper.a.get('href')
            if (product_url):
                self.product_urls.add(product_url)
                # print(self.product_urls)

    # 得到每一个页面的图片和一些数据，由于这是aiax加载的，因此前面一段的img属性是src，后面的属性是data-lazy-img
    def get_src_imgs_data(self):
        # self.search_urls = self.search_urls.format(str(self.search_page), ','.join(self.pids))
        # print(self.search_urls)
        html = requests.get(self.url, headers=self.headers)
        html.encoding = 'utf-8'
        # html = self.get_html()
        soup = BeautifulSoup(html.text, 'lxml')
        # divs = soup.find_all("li", class_='gl-item')  # 图片
        divs = soup.find_all(class_=re.compile("gl-item.*"))
        # divs_prices = soup.find_all("div", class_='p-price')   #价格
        for div in divs:
            img_1 = div.find("img").get('data-lazy-img')  # 得到没有加载出来的url
            price = div.find("strong").get_text()
            if price == "￥":
                price = "￥" + div.find("strong").get('data-price')
            keyword_Upper = div.find("div", class_='p-name p-name-type-2')
            keyword = keyword_Upper.a.em.get_text()
            keywords = keyword.split(" ")[0].split("（")[0].split("(")
            brand = keywords[0]
            print("brand is %s" % brand)
            # keyword = div.select('a > em')
            print("keyword is %s" % keyword)
            img_2 = div.find("img").get("src")  # 得到已经加载出来的url
            title = div.find("a").get("title")
            # print("title is %s" % title)
            link = div.find("a").get("href")
            # print("link is %s" % link)
            commentTag = div.find('div', attrs={'class': 'p-commit'})
            commentNum = commentTag.strong.get_text()
            # print("commentNum is %s" % commentNum)
            data_pid = div.get("data-sku")
            print("data_pid is %s" % data_pid)
            if img_1:
                print(img_1)
                # self.sql.save_img(data_pid, brand, price, commentNum, keyword, title, link, img_1)
                # self.img_urls.add(img_1)
            if img_2:
                print(img_2)
                # self.sql.save_img(data_pid, brand, price, commentNum, keyword, title, link, img_2)
                # self.img_urls.add(img_2)
                # print("--------------------------------------------------")

    def get_product_info_data(self):
        for u in self.product_urls:
            # pat = r'.*html$'
            if (str(u).endswith(".html")):
                # print("url is %s" % url)
                url = "https:" + u
                # print("urll is %s" % url)
                html = requests.get(url, headers=self.headers)
                html.encoding = 'gbk'
                soup = BeautifulSoup(html.text, 'lxml')
                product_brand_upper = soup.find(id="parameter-brand")
                product_brand = product_brand_upper.li.get('title')
                # print(product_brand)
                product_info = soup.find("ul", class_="parameter2 p-parameter-list").get_text().strip()
                product_info_list = product_info.split("\n")
                # print("product_info_list is %s" % product_info_list)
                product_name = product_info_list[0].split("：")[1]
                # print("product_name is %s" % product_name)
                product_id = product_info_list[1].split("：")[1]
                # print("produc_id is %s" % product_id)
                # self.sql.save_product_info(product_id, product_brand, product_name, product_info)
            else:
                continue

    def get_product_comments(self):
        pagesize = 10
        s = requests.session()
        for i in self.pids:
            pageno = 0
            product_id = i
            product_url = "https://sclub.jd.com/comment/productPageComments.action?productId=" + product_id + "&score=0&sortType=3&page=0&pageSize=10"
            html = requests.get(product_url, headers=self.headers).text
            try:
                bjson = json.loads(html)
                commentsummary = bjson['productCommentSummary']
                comment_num = commentsummary['commentCount']
                print("comment_num is %d" % comment_num)
                if int(comment_num) % 10 == 0:
                    comment_page_num = int(int(comment_num) / pagesize)
                else:
                    comment_page_num = int(int(comment_num) / pagesize) + 1
                print("comment_page_num is %d" % comment_page_num)
            except:
                print("解析发生错误。。。")
            try:
                while pageno <= comment_page_num:
                    comment_url = "https://sclub.jd.com/comment/productPageComments.action?productId=" + product_id + "&score=0&sortType=5&page=" + str(
                            pageno) + "&pageSize=10"
                    html = requests.get(comment_url, headers=self.headers).text
                    bjson = json.loads(html)
                    for comment in bjson['comments']:
                        user_id = comment['id']
                        user_name = comment['nickname']
                        comment_content = comment['content']
                        creationTime = comment['creationTime']
                        referenceName = comment['referenceName']
                        print("product_id is %s" % product_id)
                        print("user_id is %s" % user_id)
                        print("user_name is %s" % user_name)
                        print("comment_content is %s" % comment_content)
                        print("creationTime is %s" % creationTime)
                        print("referenceName is %s" % referenceName)
                        self.sql.save_product_comment(product_id, user_id, user_name, comment_content, referenceName,creationTime)
                    pageno += 1
            except:
                print("解析发生错误...")

    def main(self):
        self.get_pids()
        self.get_product_url()
        self.get_src_imgs_data()
        # print(len(self.img_urls))
        print("print len is %d" % len(self.product_urls))
        self.get_product_info_data()
        self.get_product_comments()
        print("------------------------------------------------------------------------------------")


if __name__ == '__main__':
    threads = []
    for i in range(1, 2):
        page = i * 2 - 1  # 这里每一页对应的都是奇数，但是ajax的请求都是偶数的，所有在获取扩展的网页时都要用page+1转换成偶数
        t = threading.Thread(target=spiders(page).main, args=[])
        threads.append(t)
    for t in threads:
        t.start()
        t.join()
    print("end")
