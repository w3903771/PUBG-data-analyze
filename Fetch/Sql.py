# -*- codeing = utf-8 -*-
# @Time : 2021-07-09 17:21
# @Author : cAMP-Cascade-DNN
# @File : Sql.py
# @Software : Pycharm
# @Contact: qq:1071747983
#          mail:wuxiaolong8001@163.com

# -*- 功能说明 -*-

#

# -*- 功能说明 -*-
import pymysql as sql

class MySQL_Connect:
    def __init__(self):
        self.write_jud = 1

        # 加载数据库
        # 创建服务器连接对象(服务端的IP)
        self.con = sql.Connect(
            host="39.106.75.227",
            user="root",
            password="root",
            database="sign_in",
            port=3308,
            charset='utf8'
        )

    # 读取数据库
    def Sql_Read_All(self):
        # 创建游标对象
        cursor = self.con.cursor()

        sql = 'SELECT class_id, class_name FROM `class_list`'
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        return result