# -*- coding = utf-8 -*-
# @Time : 2021/7/8 23:12
# @Author :　James
# @File : Pratice_1.py
# @Software: PyCharm
from chicken_dinner.pubgapi import PUBG, pubg

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ZWI0MDE5MC1jMWM3LTAxMzktNjlhNC01OWQ0NjUzOTgwNGUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjI1NzEzNTQzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImFpIn0.3Qxh94TZATIBIixI_WqAwma0fUI0vuxcc4bAeXepPrQ"
pubg = PUBG(api_key=api_key, shard="steam")

players = pubg.players_from_names("chocoTaco")

player = players[0]

print(player)
