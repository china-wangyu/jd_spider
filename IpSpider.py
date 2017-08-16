# _*_ coding:utf-8 _*_
"""
auth: sphper@126.com
data: 2017/6/29 11:43
V :   1.0
"""

from bs4 import BeautifulSoup
import requests
import random

class IPSpider(object):
    """
    爬虫代理IP
    """
    def __init__(self):
        self.url = 'http://www.xicidaili.com/nn/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        ip_list = self.get_ip_list(self.url,self.headers)
        ip = self.get_random_ip(ip_list)
        self.ip = ip
    def get_ip_list(self, url, headers):
        """
        获取代理IP列表
        :param url:获取代理IP网站
        :param headers:网站头部信息
        :return:代理IP集合
        """
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)
        return ip_list

    def get_random_ip(self,ip_list):
        """
        获取代理随机IP
        :param ip_list: 代理IP集合
        :return: 随机IP
        """
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        proxy_ip = random.choice(proxy_list)
        proxies = {"http": proxy_ip}
        return proxies
