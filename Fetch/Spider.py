# -*- codeing = utf-8 -*-
# @Time : 2021-07-09 2:08
# @Author : cAMP-Cascade-DNN
# @File : idSteal.py
# @Software : Pycharm
# @Contact: qq:1071747983
#          mail:wuxiaolong8001@163.com

# -*- 功能说明 -*-

# 设定爬虫结构 进行爬虫数据本地保存与数据库上传

# -*- 功能说明 -*-

from queue import Queue
from Selenium import Selenium
from Sql import DbConnect
import os
import sys
import time
import configparser
import pandas as pd


class Spider:

    # 初始化爬虫与数据列表 初始化数据库对象
    def __init__(self):

        # 获取项目文件夹路径用于用户数据保存
        if getattr(sys, 'frozen', False):
            self.dirPath = os.path.dirname(sys.executable)
        elif __file__:
            self.dirPath = os.path.dirname(os.path.abspath(__file__))
        self.dirPath = os.path.dirname(self.dirPath)

        # 读取配置文件
        cf = configparser.ConfigParser()
        cf.read(os.path.join(self.dirPath, "config.ini"))

        # 获取种子
        seed = cf.get("spider", 'seed')

        self.a=Selenium()
        # 待爬取用户队列
        self.userQueue = Queue(maxsize=300)
        self.userQueue.put(seed)
        # 总爬取用户列表
        self.userList = []
        # 单次爬取用户列表
        self.childList = []
        # 已爬取用户数
        self.userCount = 0
        self.baseUrl = 'https://pubg.op.gg/user/'

        # 初始化数据库对象
        self.db = DbConnect()

        self.savePath = os.path.join(self.dirPath, 'username.csv')

    # 设定爬取结构 共计爬取约1w用户信息
    def run(self):
        '''断点回溯
        with open(self.savePath, 'r', encoding="utf-8") as csvFile:  # 读取用户信息文件并存储在列表中
            reader = csv.reader(csvFile)
            rows = [row for row in reader]

        for row_player in rows:  # 读取列表中的用户信息 加入已爬取用户列表
            self.userList.append(row_player[1])

        # 更新用户数
        self.userCount = len(self.userList)
        '''

        # 第一次扩展 从种子用户进行400场次爬取
        url = os.path.join(self.baseUrl, self.userQueue.get())
        sel = Selenium()
        list = sel.run(url)
        time.sleep(0.2)
        self.childList = []
        for i in list:
            # 筛选非重复用户加入待查询队列与用户列表
            if i not in self.userList and i != 'None' and i != seed:
                self.userList.append(str(i))
                self.childList.append(str(i))
                self.userQueue.put(i)
                self.userCount += 1
                print('第一次扩展 当前第' + str(self.userCount) + '人')
        # 数据清洗 存储
        self.dataCleaning()
        self.save()
        time.sleep(1)

        # 第二次扩展 从待爬取用户队列进行拓展
        length = self.userQueue.qsize()
        print(length)
        id = 0
        for i in range(length):
            id += 1
            url = os.path.join(self.baseUrl, self.userQueue.get())
            # 输入待爬取网址 返回用户列表
            sel = Selenium()
            list1 = sel.run(url)
            self.childList = []
            for i in list1:
                # 筛选合法用户加入用户列表 重复数据后续再处理
                if i not in self.userList and i != 'None' and i != seed:
                    self.userList.append(i)
                    self.childList.append(i)
                    self.userCount += 1
                    print('第二次拓展 当前进度 ' + str(id) + "/" + str(length) +
                          '当前第' + str(self.userCount) + '人')
            self.dataCleaning()
            self.save()

        self.db.close()

    # 数据清洗与数据库存贮
    def dataCleaning(self):
        # 去除无用用户名 #unknown 0
        self.userList.remove('#unknown')
        self.userList.remove('0')
        self.userCount = len(self.userList)
        # 利用数据的有序性 降低数据库插入的时间复杂度
        self.userList.sort()
        status = self.db.userInsert(self.childList)
        while status:
            status = self.db.userInsert(self.childList)

    # 数据保存到本地CSV文件
    def save(self):
        userFile = pd.Series(self.userList)
        userFile.to_csv(self.savePath, encoding='utf8')


if __name__ == "__main__":
    spider = Spider()
    spider.run()
