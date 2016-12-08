# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from chinapulp_spider import settings


class ChinapulpSpiderPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host=settings.MYSQL_HOST,
                                    port=settings.MYSQL_PORT,
                                    user=settings.MYSQL_USER,
                                    passwd=settings.MYSQL_PASSWORD,
                                    db=settings.MYSQL_DB,
                                    charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        # 检查数据库中是否已经存在数据， 并插入为存在的数据
        # 去重入库
        # 将数据存入不同的数据库， 以满足数据库的设计范式
        query = "INSERT INTO  pulp (index_kind, indice, change_ratio, date_mon, isUP) VALUES (%s, %s, %s, %s, %s)"
        if self.isInMySQL(item):
            pass
        else:
            try:
                self.cur.execute(
                    query,
                    (item['index_kind'], float(item['index']), float(item['change_ratio']), item['date'], self.isUp(item['pic']))
                )
            # log.msg('data added to mongodb database', level=log.DEBUG, spider=spider)
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
            self.commit()
        return item  # 这个return只是在cmd中返回数据

    def isInMySQL(self, item):
        # 检查该条数据是否已经存在数据库中
        query = "SELECT index_kind, date_mon FROM pulp WHERE index_kind = %s AND date_mon = %s"
        self.cur.execute(query, (item['index_kind'], item['date']))
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False

    def isUp(self, pic_url):
        # 根据图片的url判断涨幅是上升还是下降
        if pic_url == '/skin/default/image/up.gif':
            return 1
        else:
            return 0


    # 这里的游标和数据库不需要关闭吗？
    # cur.close() 之后，conn.close() 之后， 只能插入一条数据，随后读取数据库出现错误。
    def commit(self):
        self.conn.commit()


