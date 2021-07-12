# -*- codeing = utf-8 -*-
# @Time : 2021-07-12 17:21
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
import csv
import time
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
    def deathInsert(self, list):
        print('开始死亡数据上传')
        # 创建游标对象
        cursor = self.con.cursor()
        try:
            # 对多条sql语句进行合并
            sql = "insert ignore into deathinfo values "
            for i in list:
                sql += '(' + i[0] + ",'" + i[1] + "','" + i[2] + "'," + i[3] + "," + i[4] + "," + i[5] + "," + i[
                    6] + "),"
            sql = sql[:-1] + ';'
            # print(sql)
            cursor.execute(sql)
            self.con.commit()
            print("上传完毕")
            cursor.close()
            return 0
        except Exception as e:
            print(e)
            self.con.rollback()
            return 1

    def erangelInsert(self, list):
        # 创建游标对象
        cursor = self.con.cursor()
        print('开始海岛数据上传')
        try:
            # 对多条sql语句进行合并
            sql = "insert ignore into erangelinfo values "
            for i in list[1:]:
                sql += '(' + "'" + i[0] + "'," + i[1] + '),'
            sql = sql[:-1] + ';'
            # print(sql)
            cursor.execute(sql)
            self.con.commit()
            print("上传完毕")
            cursor.close()
            return 0
        except Exception as e:
            print(e)
            self.con.rollback()
            return 1

    def finnalInsert(self, list):
        # 创建游标对象
        cursor = self.con.cursor()
        print('开始全体数据上传')
        try:
            # 对多条sql语句进行合并
            sql = "insert ignore into finnalinfo values "

            for i in list[:50001]:
                sql += '(' + i[0] + ",'" + i[1] + "','" + i[2] + "'," + i[3] + "," + i[4] + "," + i[5] + "," + i[
                    6] + "," + i[7] + "," + i[8] + '),'
            sql = sql[:-1] + ';'
            cursor.execute(sql)
            self.con.commit()

            print("1")

            # 对多条sql语句进行合并
            sql = "insert ignore into finnalinfo values "
            for i in list[50000:100001]:
                sql += '(' + i[0] + ",'" + i[1] + "','" + i[2] + "'," + i[3] + "," + i[4] + "," + i[5] + "," + i[
                    6] + "," + i[7] + "," + i[8] + '),'
            sql = sql[:-1] + ';'
            cursor.execute(sql)
            self.con.commit()

            print("2")

            # 对多条sql语句进行合并
            sql = "insert ignore into finnalinfo values "
            for i in list[100000:150001]:
                sql += '(' + i[0] + ",'" + i[1] + "','" + i[2] + "'," + i[3] + "," + i[4] + "," + i[5] + "," + i[
                    6] + "," + i[7] + "," + i[8] + '),'
            sql = sql[:-1] + ';'
            cursor.execute(sql)
            self.con.commit()

            print("3")

            # 对多条sql语句进行合并
            sql = "insert ignore into finnalinfo values "
            for i in list[150000:200001]:
                sql += '(' + i[0] + ",'" + i[1] + "','" + i[2] + "'," + i[3] + "," + i[4] + "," + i[5] + "," + i[
                    6] + "," + i[7] + "," + i[8] + '),'
            sql = sql[:-1] + ';'
            cursor.execute(sql)
            self.con.commit()

            print("4")

            # 对多条sql语句进行合并
            sql = "insert ignore into finnalinfo values "
            for i in list[200000:]:
                sql += '(' + i[0] + ",'" + i[1] + "','" + i[2] + "'," + i[3] + "," + i[4] + "," + i[5] + "," + i[
                    6] + "," + i[7] + "," + i[8] + '),'
            sql = sql[:-1] + ';'
            cursor.execute(sql)
            self.con.commit()

            print('传输完毕')
            cursor.close()
            return 0
        except Exception as e:
            print(e)
            self.con.rollback()
            return 1

    def miramarInsert(self, list):
        # 创建游标对象
        cursor = self.con.cursor()
        print('开始沙漠数据上传')
        try:
            # 对多条sql语句进行合并
            sql = "insert ignore into miramarinfo values "
            for i in list[1:]:
                sql += '(' + "'" + i[0] + "'," + i[1] + '),'
            sql = sql[:-1] + ';'
            # print(sql)
            cursor.execute(sql)
            self.con.commit()
            print('传输完毕')
            cursor.close()
            return 0
        except Exception as e:
            print(e)
            self.con.rollback()
            return 1


class Sql:
    def __init__(self):
        self.db = DbConnect()

        if getattr(sys, 'frozen', False):
            self.Path = os.path.dirname(sys.executable)
        elif __file__:
            self.Path = os.path.dirname(os.path.abspath(__file__))

    def run(self):
        deathPath = os.path.join(self.Path, 'death_player_detail.csv')
        erangelPath = os.path.join(self.Path, 'erangel_weapon.csv')
        finnalPath = os.path.join(self.Path, 'finnal_player_detail.csv')
        miramarPath = os.path.join(self.Path, 'miramar_weapon.csv')

        with open(deathPath, 'r', encoding="utf-8") as csvFile1:
            reader = csv.reader(csvFile1)
            rows1 = [row for row in reader]

        with open(erangelPath, 'r', encoding="utf-8") as csvFile2:
            reader = csv.reader(csvFile2)
            rows2 = [row for row in reader]

        with open(finnalPath, 'r', encoding="utf-8") as csvFile3:
            reader = csv.reader(csvFile3)
            rows3 = [row for row in reader]

        with open(miramarPath, 'r', encoding="utf-8") as csvFile4:
            reader = csv.reader(csvFile4)
            rows4 = [row for row in reader]

        self.db.deathInsert(rows1)
        time.sleep(5)
        self.db.erangelInsert(rows2)
        time.sleep(5)
        self.db.finnalInsert(rows3)
        time.sleep(5)
        self.db.miramarInsert(rows4)


if __name__ == "__main__":
    sql = Sql()
    sql.run()
