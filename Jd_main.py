# _*_ coding:utf-8 _*_

"""
date : 2017-6-17 14:55
auth : 青雉
version : 1.1
"""

import Jd_spider, Jd_mysql, load

if __name__ == '__main__':

    Jd_Mysql = Jd_mysql.JdMysql()
    Jd_Model = Jd_Mysql.Table()
    num = int(raw_input("请输入您想爬取的页数："))
    if num == '':
        num = int(raw_input("请重新输入您想爬取的页数："))
    param = {
        "url" : "https://search.jd.com/search?keyword=%E7%99%BD%E9%85%92&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%99%BD%E9%85%92&ev=3221_74564%402762_71141%40&s=58&click=0&page=",

        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"
        },
        "page_num": num,
        "goods_count": 1,
        "page_count": 1
    }

    Jd = Jd_spider.JdSpider(Jd_Model, param ,proxy=False)
    print "您爬取的网址是：%s" % Jd.param['url']
    if Jd.proxy != '':
        print "您使用的代理IP是：[ %s ]" % str(Jd.proxy['http'])
    print "您设置的页数是：%s" % Jd.param['page_num']
    print "您爬取的页数是：%s" % Jd.param['page_count']
    print "您爬取的商品数是：%s" % Jd.param['goods_count']
    print "您爬取每件商品间隔是：%s" % Jd.time_interval_spider
