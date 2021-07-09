# -*- coding = utf-8 -*-
# @Time : 2021/7/8 23:19
# @Author :　James
# @File : Pratice_3.py
# @Software: PyCharm
from chicken_dinner.pubgapi import PUBGCore

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ZWI0MDE5MC1jMWM3LTAxMzktNjlhNC01OWQ0NjUzOTgwNGUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjI1NzEzNTQzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImFpIn0.3Qxh94TZATIBIixI_WqAwma0fUI0vuxcc4bAeXepPrQ"
pubgcore = PUBGCore(api_key, "pc-na")
shroud = pubgcore.players("chocoTaco", "shroud")
print(shroud)