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
from selenium import webdriver
from selenium.webdriver import ActionChains

#def main():
path='C:\Program Files (x86)\Google\Chrome Beta\Application\chromedriver.exe'
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options,executable_path=path)

browser.get("https://pubg.op.gg/user/AixLeft")
# 鼠标移动到 ac 位置
# ac = driver.find_element_by_xpath('element')
# ActionChains(driver).move_to_element(ac).perform()

# browser.find_element_by_css_selector(".form-control").send_keys("AixLeft")
browser.find_element_by_css_selector(".matches-item__btn.matches-item__btn--members.matches-item__btn--members-win").click()

#main()