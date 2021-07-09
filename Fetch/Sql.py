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
import pymysql as sql


class DbConnect:
    def __init__(self):

        self.con = sql.Connect(
            host="39.106.75.227",
            user="root",
            password="root",
            database="pubg_data",
            port=3308,
            charset='utf8'
        )

    # 使用事务将list插入数据库 并对错误进行回滚操作
    def userInsert(self, list):
        # 创建游标对象
        cursor = self.con.cursor()
        try:
            sql = "insert into 'userinfo' values "
            for i in list:
                sql += '(' + str(i) + '),'
            sql[-1] = ';'
            cursor.execute(sql)
            cursor.commit()
            cursor.close()
            return 0
        except Exception as e:
            print(e)
            self.con.rollback()
            return 1


    def close(self):
        self.con.close()