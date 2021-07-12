# -*- codeing = utf-8 -*-
# @Time : 2021-07-09 17:21
# @Author : cAMP-Cascade-DNN
# @File : Sql.py
# @Software : Pycharm
# @Contact: qq:1071747983
#          mail:wuxiaolong8001@163.com

# -*- 功能说明 -*-

# 对批量用户名进行数据存储

# -*- 功能说明 -*-
import os
import sys
import configparser
import pymysql as sql


class DbConnect:
    def __init__(self):

        if getattr(sys, 'frozen', False):
            Path = os.path.dirname(sys.executable)
        elif __file__:
            Path = os.path.dirname(os.path.abspath(__file__))
        Path = os.path.dirname(Path)

        cf = configparser.ConfigParser()
        cf.read(os.path.join(Path, "config.ini"))

        host = cf.get("mysql1", "host")
        user = cf.get("mysql1", "user")
        password = cf.get("mysql1", "password")
        database = cf.get("mysql1", "database")
        port = cf.getint("mysql1", "port")
        charset = cf.get("mysql1", "charset")

        # 数据库连接
        self.con = sql.Connect(host=host, user=user, password=password, database=database, port=port, charset=charset)

    # 使用事务将list插入数据库 并对错误进行回滚操作
    def userInsert(self, list):
        # 创建游标对象
        cursor = self.con.cursor()
        try:
            # 对多条sql语句进行合并
            sql = "insert ignore into userinfo values "
            for i in list:
                sql += '(' + "'" + str(i) + "'" + '),'
            sql = sql[:-1] + ';'
            # print(sql)
            cursor.execute(sql)
            self.con.commit()
            cursor.close()
            return 0
        except Exception as e:
            print(e)
            self.con.rollback()
            return 1

    def close(self):
        self.con.close()
