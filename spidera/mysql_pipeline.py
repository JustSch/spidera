import pymysql.cursors
from scrapy.exceptions import DropItem
import logging


class MySQLPipeline(object):

    def open_spider(self, spider):
        print("opened")

    def __init__(self):

        self.connection = pymysql.connect(user='dbUser, password='dbPassowrd',
                                          host='dbHost',
                                          database='dbName',
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()


    def process_item(self, item, spider):

        logger = logging.getLogger()
        logger.debug("This is a warning")
        try:
            sql = """CALL ScrapedData(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            val = (item['link_url'], item['link_title'], item['link_description'].strip(), item['last_update'],item['word1'], item['word2'], item['word3'], item['word4'], item['word5'])
             
            self.cursor.execute(sql, val)
            self.connection.commit()
            
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            print(self.cursor._last_executed)
       

    def close_spider(self, spider):
        print("close")
        self.cursor.close()
        self.connection.close()
