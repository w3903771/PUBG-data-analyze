# -*- coding = utf-8 -*-
# @Time : 2021/7/9 10:30
# @Author :　Hiram
# @File : Selenium1.py
# @Software: PyCharm

from time import sleep

from lxml import etree
from selenium import webdriver


class Selenium:
    def __init__(self):

        # 设定浏览器驱动位置
        path = 'C:\Program Files (x86)\Google\Chrome Beta\Application\chromedriver.exe'
        # 初始化驱动
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=options, executable_path=path)
        self.browser.maximize_window()
        # 不指定驱动文件位置
        # self.self.browser = webdriver.Chrome(options=options)

    def close(self):
        self.browser.quit()

    def run(self, url1):
        url = url1
        self.browser.get(url)
        sleep(1)

        # 置爬取状态码真
        status = True
        # 进行400场次比赛抓取 点击20次加载“more” 每次爬取加载的20条比赛用户信息
        for i in range(20):
            if status:
                # 拉倒页面底部 避免底部广告干扰
                js = "var q=document.documentElement.scrollTop=10000"
                self.browser.execute_script(js)
                # 使用try..except 解决数据不够以及按钮没加载的情况 将直接跳过
                try:
                    e1 = self.browser.find_element_by_css_selector(".total-played-game__btn.total-played-game__btn--more")
                    self.browser.execute_script("arguments[0].click();", e1)
                    sleep(1)
                    for j in range(20):
                        self.browser.find_element_by_css_selector(".matches-item__btn.matches-item__btn--members").click()
                    self.browser.implicitly_wait(20)
                except:
                    status = False
            else:
                break

        baseurl = self.browser.page_source
        tree = etree.HTML(baseurl)
        list = tree.xpath('//*[@id="matchDetailWrap"]/div[3]/div[1]/div/div/div[2]/ul/li')
        # 总比赛用户信息
        l_all = []
        for i in list:
            m = i.xpath('./div[1]/div[6]/div/div/ul/li')
            for li in m:
                try:
                    n1 = li.xpath('./div/a/text()')[0]
                except:
                    n1 = None
                    pass
                l_all.append(str(n1))
        while [] in l_all:
            l_all.remove([])
        # 输出总获取用户名数
        print(len(l_all))
        sleep(1)
        self.browser.close()
        # 返回获取用户名列表
        return l_all
