# -*- coding = utf-8 -*-
# @Time : 2021/7/8 23:17
# @Author :　James
# @File : Pratice_2.py
# @Software: PyCharm
from chicken_dinner.pubgapi import PUBG

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ZWI0MDE5MC1jMWM3LTAxMzktNjlhNC01OWQ0NjUzOTgwNGUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjI1NzEzNTQzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImFpIn0.3Qxh94TZATIBIixI_WqAwma0fUI0vuxcc4bAeXepPrQ"
pubg = PUBG(api_key, "pc-na")
shroud = pubg.players_from_names("shroud")[0]
shroud_season = shroud.get_current_season()
squad_fpp_stats = shroud_season.game_mode_stats("squad", "fpp")
print(squad_fpp_stats)