# _*_ coding:utf-8 _*_

"""
date : 2017-6-17 14:55
auth : 青雉
version : 1.1
"""

import time,xlwt,urllib,os,pymysql

class Load():
    """
    下载类
    """

    def export_xls(host, user, password, dbname, table_name, outputpath):
        conn = pymysql.connect(host, user, password, dbname, charset='utf8')
        cursor = conn.cursor()

        count = cursor.execute('select * from ' + table_name)
        print count
        # 重置游标的位置
        cursor.scroll(0, mode='absolute')
        # 搜取所有结果
        results = cursor.fetchall()

        # 获取MYSQL里面的数据字段名称
        fields = cursor.description
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('table_' + table_name, cell_overwrite_ok=True)

        # 写上字段信息
        for field in range(0, len(fields)):
            sheet.write(0, field, fields[field][0])

        # 获取并写入数据段信息
        row = 1
        col = 0
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields)):
                sheet.write(row, col, u'%s' % results[row - 1][col])

        workbook.save(outputpath)



    #F:\python\img
    def save_img(self,file_path,img_src):
        """
        保存图片
        :param file_path: 下载路径
        :param img_src:  图片src路径
        :return:
        """
        if os.path.exists(file_path) == False:  # 如果这个文件夹不存在
            os.makedirs(file_path)  # 创建这个文件夹
        imgname = img_src.rsplit("/", 1)[1]  # 图片名
        dowpath = os.path.join(file_path, imgname)  # 拼接,得到下载地址
        self.img(img_src, dowpath)  # 调用下载函数
        time.sleep(3)  # 让爬虫休息1秒
        print "下载完成"


    def img(self,img_path,save_path):
        """
           下载图片
           :param img_path: 存储图片路径
           :param save_img_name: 图片名称
           """
        urllib.urlretrieve(img_path, save_path)  # 下载图片


