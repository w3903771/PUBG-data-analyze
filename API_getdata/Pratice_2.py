# -*- coding = utf-8 -*-
# @Time : 2021/7/8 23:17
# @Author :　James
# @File : Pratice_2.py
# @Software: PyCharm
from chicken_dinner.pubgapi import PUBG
import Get_data

datalist = {'Tom': {'player_kills': 1}}

class Player_Detail():
    def __init__(self, datalist, name, player_kills=None):
        self._player_kills = datalist[player_kills ]
        self._team_placement = datalist[name]

