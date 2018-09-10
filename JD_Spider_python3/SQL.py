# coding:utf-8
import pymysql as db


# 将得到的数据存入数据库中mysql
class save_mysql:
    def __init__(self):
        self.user = 'root'
        self.password = 'root'
        self.host = 'localhost'
        self.database = 'test'

    def get_connection(self):
        return db.connect(user="root", passwd="root", host="10.88.20.201", db="test", charset="utf8")

    def save_img(self, data_pid, brand, price, commentNum, keyword, title, link, img):
        conn = self.get_connection()
        cursor = conn.cursor()
        # insertSql = """insert into JD_kongtiao(data_pid,img,price,keyword,title,link,commentNum) values(%s,%s,%s,%s,%s,%s,%s)""" % args
        # data = (data_pid, img, price, keyword, title, link, commentNum)
        cursor.execute(
                "insert into JD_kongtiao(data_id,brand,price,commentNum,keyword,title,item_link, pic_link) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                (str(data_pid), str(brand), str(price), str(commentNum), str(keyword), str(title), str(link), str(img)))
        # cursor.execute(insertSql)
        conn.commit()

    def save_product_info(self, product_id, product_brand, product_name, product_info):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO JD_kongtiao_info(data_id,brand, product_name, product_info ) VALUES (%s, %s, %s, %s)",
                (str(product_id), str(product_brand), str(product_name), str(product_info))
        )
        conn.commit()

    def save_product_comment(self, product_id, user_id, user_name, comment_content, referenceName, creationTime):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO JD_kongtiao_comment(product_id, user_id, user_name, comment_content, referenceName,creationTime) VALUES (%s, %s, %s, %s, %s, %s)",
                (str(product_id), str(user_id), str(user_name), str(comment_content), str(referenceName),
                 str(creationTime))
        )
        conn.commit()
