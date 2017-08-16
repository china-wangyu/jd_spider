# _*_ coding:utf-8 _*_

"""
date : 2017-6-17 14:55
auth : 青雉
version : 1.1
"""

import peewee

class JdMysql(object):
    def __init__(self):
        self.param = {
            'host' : "localhost",
            'dbname' : 'ant',
            'user' : 'root',
            'passwd' : 'root',
            'port' : 3306,
        }
        self.conn = peewee.MySQLDatabase(
            host=self.param['host'],
            port=self.param['port'],
            user=self.param['user'],
            passwd=self.param['passwd'],
            database=self.param['dbname']
        )
    def Table(self,table='ant_jd_goods'):
        class Ant_jd_goods(peewee.Model):
            goods_name = peewee.CharField(max_length=200)
            goods_img = peewee.CharField(max_length=255)
            goods_price = peewee.CharField(max_length=30)
            goods_sale = peewee.CharField(max_length=30)
            goods_url = peewee.CharField(max_length=255)
            goods_pcate = peewee.CharField(max_length=255)
            goods_brand = peewee.CharField(max_length=100)
            goods_shop = peewee.CharField(max_length=150)
            goods_sql_addtime = peewee.CharField(max_length=30)

            class Meta:
                database = self.conn


        return  Ant_jd_goods