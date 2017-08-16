# _*_ coding:utf-8 _*_

"""
date : 2017-6-17 14:55
auth : 青雉
version : 1.1
"""
import time, urllib2,requests
from bs4 import BeautifulSoup

import IpSpider


class JdSpider(object):
    """
        创建爬虫类
    """

    def __init__(self, Jd_mysql, data, proxy=True):
        if not data:
            self.param = self.defualt_param()
        else:
            self.param = data
        if proxy == True:
            self.proxy_set()
        else:
            self.proxy = ''
        self.load_page(Jd_mysql)

    def load_one(self, url):
        """
        加载网页
        :param data: 网页header和url
        :return: 爬取的网页源代码
        """
        if self.proxy != '':
            proxy = urllib2.ProxyHandler(self.proxy)
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            try:
                request = urllib2.Request(url=url, headers=self.param['headers'])
                contect = urllib2.urlopen(request,timeout=30)
            except requests.exceptions.ConnectionError:
                self.proxy_set(status=True)
                proxy = urllib2.ProxyHandler(self.proxy)
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)
                request = urllib2.Request(url=url, headers=self.param['headers'])
                contect = urllib2.urlopen(request,timeout=30)

        else:
            request = urllib2.Request(url=url, headers=self.param['headers'])
            contect = urllib2.urlopen(request)
        return contect.read()

    def load_page(self, mysql_db):
        """
        网页page分析
        :param url: 爬去网页url
        :param num: 下载的页数
        :param src: 图片
        :return:
        """
        contect = self.load_one(self.param['url'])
        goodsArr = self.get_goods_info(contect)
        self.insert_goods_sql(mysql_db, goodsArr)
        self.param['page_count'] = self.param['page_count'] + 1
        if self.param['page_num'] > 1:
            for i in range(1, self.param['page_num']):
                self.habit(10)
                print "正在进入第", self.param['page_count'], '页'
                contect = self.load_one(self.param['url'] + str(i + 2))
                goodsArr = self.get_goods_info(contect)
                self.insert_goods_sql(mysql_db, goodsArr)
                self.param['page_count'] = self.param['page_count'] + 1

        self.stop()
        return True

    def get_goods_info(self, goodsInfoBoday):
        """
        获取商品信息
        :param goodsInfoBoday: 商品详情页面
        :return: 商品详细信息集合
        """
        soup = BeautifulSoup(goodsInfoBoday, "lxml")
        name_list = soup.select('div[class="gl-i-wrap"] > div > a > em')  # 商品名称
        goodsname_list = []
        for name in name_list:
            p_name = name.get_text().strip()
            goodsname_list.append(p_name)

        img_list = soup.select('div[class=gl-i-wrap] > div[class=p-img] > a > img')  # 商品img
        goodsimg_list = []
        for img in img_list:
            # img_path = unicode("F:/python/img/白酒/",'utf-8')
            try:
                imgname = 'https://' + img['src'].rsplit("//'", 1)[-1]  # 图片名
            except KeyError:
                imgname = 'https://' + img['data-lazy-img'].rsplit("//'", 1)[-1]  # 图片名
            # dowpath = os.path.join(img_path, imgname)

            goodsimg_list.append(imgname)
            # load.save_img(img_path,img['src'])

        price_list = soup.select('div[class=gl-i-wrap] > div[class=p-price] > strong > i')  # 商品价格
        goodsprice_list = []
        for price in price_list:
            goodsprice_list.append(price.get_text().strip())

        sale_list = soup.select('div[class=gl-i-wrap] > div[class=p-commit] > strong > a')  # 商品销量
        goodssale_list = []
        for sale in sale_list:
            goodssale_list.append(sale.get_text().strip())

        url_list = soup.select('div[class=gl-i-wrap] > div[class=p-img] > a')  # 商品img
        goodsurl_list = []
        for url in url_list:
            url_link = 'https:' + url['href'].rsplit("//'", 1)[-1]  # 图片名
            goodsurl_list.append(url_link)

        goodsArr = {
            'goods_name': goodsname_list,
            'goods_img': goodsimg_list,
            'goods_price': goodsprice_list,
            'goods_sale': goodssale_list,
            'goods_sql_addtime': unicode(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "utf-8"),
            'goods_url': goodsurl_list,
        }

        return goodsArr

    def get_goods_params(self, url):
        """
        获取商品参数
        :param goodsArr: 商品基本信息
        :return: 单个商品完整信息
        """
        boday = self.load_one(url)
        soup = BeautifulSoup(boday, "lxml")

        goods_brand = soup.select('div[class=item] > a')
        brand_name = ''
        for brand in goods_brand:
            brand_name = brand_name + '/' + brand.get_text().strip()
        brand_name = brand_name.rsplit("/", 1)[0]

        goods_shop = soup.select('div[class=name] > a')
        shop_name = ''
        for shop in goods_shop:
            shop_name = shop_name + ' ' + shop['title']

        goods_pcate = soup.select('div[class="p-parameter"] > ul[class="p-parameter-list"] > li')
        pcate_name = ""
        for pcate in goods_pcate:
            pcate_name = pcate_name + ' ' + pcate['title']

        goods_param = {
            'goods_pcate': brand_name,
            'goods_brand': pcate_name,
            'goods_shop': shop_name
        }
        return goods_param

    def insert_goods_sql(self, Ant, goodsArr):
        """
        添加爬虫爬取的商品数据
        :param Ant: 实例化的peewee表对象
        :param goodsArr: 获取的商品集合
        :param self.param['goods_count']: 商品的个数
        :return: self.param['goods_count'] 商品的个数
        """
        for (name, img, price, sale, url) in zip(goodsArr['goods_name'], goodsArr['goods_img'], goodsArr['goods_price'],
                                                 goodsArr['goods_sale'], goodsArr['goods_url']):
            print '正在获取第 ',str(self.param['goods_count']),' 件商品的信息： 商品名称- ',name
            goods_param = self.get_goods_params(url)

            Ant.create(
                goods_name=name,
                goods_img=img,
                goods_price=price,
                goods_sale=sale,
                goods_url=url,
                goods_pcate=goods_param['goods_pcate'],
                goods_brand=goods_param['goods_brand'],
                goods_shop=goods_param['goods_shop'],
                goods_sql_addtime=goodsArr['goods_sql_addtime']
            )
            self.param['goods_count'] = self.param['goods_count'] + 1

    def stop(self):
        """
        关闭爬虫
        :return:
        """
        print "感谢您的使用："
        print "- 爬虫停止工作，请重新启动爬虫 - JdSpider"
        pass

    def defualt_param(self):
        """
        默认值获取
        :return: 返回默认值
        """
        self.param = {
            "url": "http://search.jd.com/search?keyword=%E8%8C%B6&enc=utf-8&psort=3&ev=2762_32941%40&page=",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"
            },
            "page_num": 10,
            "goods_count": 1,
            "page_count": 1
        }

    def habit(self, interval_time=3):
        """
        爬虫习惯设置
        :return:
        """
        self.time_interval_spider = interval_time  # 爬虫爬取信息间隔时间，防止IP被网站限制(默认3秒)
        time.sleep(self.time_interval_spider)  # 让爬虫休息设置的时间

    def proxy_set(self, proxy={}, status=False):
        """
        设置代理IP
        :param proxy:手动代理IP
        :return: 代理IP
        """
        if status == True:
            IP = IpSpider.IPSpider()
            ip_addr = IP.ip
        elif not proxy:
            IP = IpSpider.IPSpider()
            ip_addr = IP.ip
        else:
            ip_addr = proxy
        self.proxy = ip_addr
