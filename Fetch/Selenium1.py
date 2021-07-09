# -*- coding = utf-8 -*-
# @Time : 2021/7/9 10:30
# @Author :　Hiram
# @File : Selenium1.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import bs4
import re
import urllib.request
import sqlite3
import xlwt

def main():
    baseurl = a()
    # baseurl = "https://pubg.op.gg/user/AixLeft"
    datalist = getData(baseurl)
    print(datalist)

    savepath = "Steal-User-id.xls"
    # 3.保存数据
    # saveData(datalist, savepath)
    # askURL("https://movie.douban.com/top250?strat=")

def a():
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options)
    browser.get("https://pubg.op.gg/user/AixLeft")
    # browser.find_element_by_css_selector(".form-control").send_keys("AixLeft")
    for i in range(5):
        browser.find_element_by_css_selector(".total-played-game__btn.total-played-game__btn--more").click()
        for j in range(20):
            e1 = browser.find_element_by_css_selector(".matches-item__btn.matches-item__btn--members")
            browser.execute_script("arguments[0].click();", e1)
        browser.implicitly_wait(5)
    # html = browser.page_source()
    # html = browser.current_url
    return browser.page_source


findUser = re.compile(r'<a data-link="player-link" href="http://pubg.op.gg/user/(.*?)" class="player-ranking__player">')   # 创建正则表达式对象，表示规则（字符串模式）

# 爬取网页
def getData(baseurl):
    datalist = []
    html = askURL(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('a', class_="matches-item__layout matches-item__layout--member"):   # 查找符合要求的字符串·形成列表
        data = []
        item = str(item)

        link = re.findall(findUser, item)[0]        # re库用来通过正则表达式查找指定的字符串
        data.append(link)                           # 添加链接
        datalist.append(data)                       # 把处理好的一部电影信息放入datalist

    return datalist


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == "__main__":
    main()
    print("爬取完毕")