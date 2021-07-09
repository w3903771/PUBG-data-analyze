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
from Queue import Queue

class Spider:

    # 初始化爬虫 设定浏览器驱动与爬虫种子
    def __init__(self, seed):

        # 设定浏览器驱动位置
        path = 'C:\Program Files (x86)\Google\Chrome Beta\Application\chromedriver.exe'
        # 初始化驱动
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=options, executable_path=path)

        # 不指定驱动文件位置
        # self.browser = webdriver.Chrome(options=options)

        # 待爬取用户队列
        self.userQueue = Queue(maxsize=200)
        self.userQueue.put(seed)
        # 爬取用户列表
        self.userList = []
        # 已爬取用户数
        self.userCount = 0
        self.baseUrl = 'https://pubg.op.gg/user/'

    # 设定爬取结构 共计爬取1w次用户信息
    def run(self):

        # 第一次扩展 从种子用户进行100次爬取
        url = self.baseUrl + self.userQueue.get()
        # 输入待爬取网址 返回用户列表
        list = pq(url)
        for i in list:
            if i not in self.userList:
                self.userList.append(i)
                self.userQueue.put(i)
                self.userCount += 1

        # 第二次扩展 从待爬取用户队列进行拓展
        length = self.userQueue.qsize()
        for i in range(length):
            url = self.baseUrl + self.userQueue.get()
            # 输入待爬取网址 返回用户列表
            list = pq(url)
            for i in list:
                if i not in self.userList:
                    self.userList.append(i)
                    self.userQueue.put(i)
                    self.userCount += 1


if __name__ == "__main__":
    main()
    print("爬取完毕")
