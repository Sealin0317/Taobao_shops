# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class TaobaoprojectPipeline(object):
#     def process_item(self, item, spider):
#         return item
import pymongo
import pymysql


# class MongoPipeline(object):
#     def __init__(self, mongo_url, mongo_db):
#         self.mongo_url = mongo_url
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_url=crawler.settings.get('MONGO_URL'),
#             mongo_db=crawler.settings.get('MONGO_DB')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_url)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         name = item.__class__.__name__
#         self.db[name].insert(dict(item))
#         spider.logger.info('saving to Mongodb~~~~~~~~~~~~')
#         return item


class MysqlPipeline(object):
    def __init__(self, host, user, passwd):
        self.conn = pymysql.connect(host=host, unix_socket='/tmp/mysql.sock',
                                    user=user, passwd=passwd, db='mysql', charset='utf8')
        self.cur = self.conn.cursor()


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HOST'),
            user=crawler.settings.get('USER'),
            passwd=crawler.settings.get('PASSWD')
        )

    def open_spider(self, spider):
        self.cur.execute("USE taobao;")

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute(
            "INSERT INTO t4 (location,k1,k2,title,rank,rate,sales,amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                item['location'],
                item['k1'],
                item['k2'],
                item['title'],
                item['rank'],
                item['rate'],
                item['sales'],
                item['amount']
            ))
        self.cur.connection.commit()
        spider.logger.info('Saving to Mysql-----------------------')
        return item

        # # set mysql
        # conn = pymysql.connect(host='106.14.196.40', unix_socket='/tmp/mysql.sock',
        #                        user='root', passwd='mysqlroot', db='mysql', charset='utf8')
        # cur = conn.cursor()
        # cur.execute("USE taobao;")
        #
        #
        # # save to mysql
        # def save_to_mysql(k1, k2, title, location, rank, rate, sales, amount):
        #     print('begin to save to mysql~~~~~~~', k1, k2, title, location, rank, rate, sales, amount)
        #     cur.execute("INSERT INTO t2 (k1,k2,title,location,rank,rate,sales,amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        #                 (k1, k2, title, location, rank, rate, sales, amount))
        #     cur.connection.commit()
