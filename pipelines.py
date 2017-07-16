# -*- coding: utf-8 -*-
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request

import MySQLdb
import MySQLdb.cursors
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MistorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = 'localhost',
            db = 'python',
            user = 'root',
            passwd = '915348696',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        sql = "insert into miweb_mistore (app_name, app_size, app_version, app_updatetime, app_package, app_company, company_tel, company_email, company_address, company_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item['app_name'], item['app_size'], item['app_version'], item['app_updatetime'], item['app_package'], item['app_company'], item['company_tel'], item['company_email'], item['company_address'], item['company_url'])
        tx.execute(sql,  params)

    def handle_error(self, failue):
         print 'lyh %s' % failue

