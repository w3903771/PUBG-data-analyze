# -*- codeing = utf-8 -*-
# @Time : 2021-07-09 2:08
# @Author : cAMP-Cascade-DNN
# @File : idSteal.py
# @Software : Pycharm
# @Contact: qq:1071747983
#          mail:wuxiaolong8001@163.com

# -*- 功能说明 -*-

#

# -*- 功能说明 -*-
from Sql import DbConnect
from queue import Queue
import os
import sys
import pandas as pd


class Spider:

    # 初始化爬虫 设定浏览器驱动与爬虫种子
    def __init__(self, seed):

        # 设定浏览器驱动位置
        path = 'C:\Program Files (x86)\Google\Chrome Beta\Application\chromedriver.exe'
        # 初始化驱动
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=options, executable_path=path)

        不指定驱动文件位置
        self.browser = webdriver.Chrome(options=options)

        # 待爬取用户队列
        self.userQueue = Queue(maxsize=200)
        self.userQueue.put(seed)
        # 爬取用户列表
        self.userList = []
        # 已爬取用户数
        self.userCount = 0
        self.baseUrl = 'https://pubg.op.gg/user/'

        # 初始化数据库对象
        self.db = DbConnect()

    # 设定爬取结构 共计爬取约1w次用户信息
    def run(self):

        # 第一次扩展 从种子用户进行100次爬取
        url = self.baseUrl + self.userQueue.get()
        # 输入待爬取网址 返回用户列表
        list = pq(url)
        for i in list:
            # 筛选非重复用户加入查询队列与用户列表
            if i not in self.userList and i != '#Unknow':
                self.userList.append(i)
                self.userQueue.put(i)
                self.userCount += 1
                print(self.userCount)

        # 第二次扩展 从待爬取用户队列进行拓展
        length = self.userQueue.qsize()
        for i in range(length):
            url = self.baseUrl + self.userQueue.get()
            # 输入待爬取网址 返回用户列表
            list = pq(url)
            for i in list:
                # 筛选合法用户加入用户列表 重复数据后续再处理
                if i != '#Unknow':
                    self.userList.append(i)
                    self.userCount += 1
                    print(self.userCount)

    # 数据清洗与数据库存贮
    def dataCleaning(self):
        # list去重
        self.userList = list(set(self.userList))
        self.userCount = self.userList.size()
        # 利用数据的有序性 降低数据库插入的时间复杂度
        self.userList.sort()
        status = True
        while status:
            status = self.db.userInsert(self.userList)
        self.db.close()

    # 数据保存到本地文件
    def save(self, path):
        path = os.path.join(path, 'username.csv')
        userFile = pd.Series(self.userList)
        userFile.to_csv(path, sep='\n', index_label=False, encoding='utf8', compression='gzip')


if __name__ == "__main__":

    seed = 'AixLeft'

    # 获取项目文件夹路径用于用户数据保存
    if getattr(sys, 'frozen', False):
        savePath = os.path.dirname(sys.executable)
    elif __file__:
        savePath = os.path.dirname(os.path.abspath(__file__))
    savePath = os.path.dirname(savePath)

    spider = Spider(seed)
    spider.run()
    spider.save(savePath)
