# -*- coding = utf-8 -*-
# @Time : 2021/7/8 23:12
# @Author :　James
# @File : Get_data.py
# @Software: PyCharm
from chicken_dinner.pubgapi import PUBGCore,PUBG, pubg
import csv
import os
import sys

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ZWI0MDE5MC1jMWM3LTAxMzktNjlhNC01OWQ0NjUzOTgwNGUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjI1NzEzNTQzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImFpIn0.3Qxh94TZATIBIixI_WqAwma0fUI0vuxcc4bAeXepPrQ"
pubg = PUBG(api_key=api_key, shard="steam")    # 创建PUBG实例，api_key(API秘钥），shard（对服务器进行获取）

map_list = ["Erangel (Remastered)", "Miramar"]

def main():

    if getattr(sys, 'frozen', False):      # 建立用户文件路径
        Path = os.path.dirname(sys.executable)
    elif __file__:
        Path = os.path.dirname(os.path.abspath(__file__))
    Path=os.path.dirname(Path)
    path=os.path.join(Path,'username.csv')

    with open(path, 'r', encoding="utf-8") as csvfile:   # 读取用户信息文件并存储在列表中
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    for row_player in rows:    # 读取列表中的用户信息
        name = row_player[1]

        players = pubg.players_from_names(name)  # 创建玩家实例
        player = players[0]

        for i in range(10):
            try:
                if i == 0:
                    print("玩家 '" + player.name + "' 的近期参加的比赛所有情况： ")

                match = pubg.match(player.match_ids[i])    # 获取玩家近期比赛ID
                telemetry = match.get_telemetry()    # 创建一局比赛中的所有日志集合实例

                map_Name = get_Map_Name(telemetry)              # 筛选只获取海岛和沙漠地图信息
                if map_Name not in map_list:
                    continue

                player_Num = get_Player_Num(telemetry)          # 保存比赛人数信息
                team_Num = get_Team_Num(telemetry)              # 保存比赛队伍信息
                game_Mode = get_Game_Mode(match)                # 保存比赛模式信息
                game_Time = get_Game_Time(match)                # 保存比赛持续时间信息
                player_ride_distance = get_Vehicle_Ride(telemetry)
                # game_attack = get_Game_Attack(telemetry)
                # get_Player_Death_Postion(telemetry)
                killer_weapon_detail = find_weapon_kills(telemetry)



                print("第 " + str(i+1) + " 场游戏中 : ")
                print("\t\t地图为： " + map_Name)
                print("\t\t游戏模式为： " + game_Mode)
                print("\t\t玩家人数为： " + str(player_Num))
                print("\t\t队伍数量为： " + str(team_Num))

                text = find_weapon_kills(telemetry)
                print(text)
                for kill_total, number in text.items():  # 记录每种武器击杀的次数
                    print(kill_total, " 击杀数为： ", number)
                # print(player_ride_distance)

                # for weapon_name in killer_weapon_detail.keys():
                #     total = killer_weapon_detail[weapon_name]['kills_total']
                #     print("\n\t\t武器 ‘" + weapon_name + "' 的击杀信息为：")
                #
                #     for num in range(1, total+1):
                #         killer_location_x = killer_weapon_detail[weapon_name][num]["killer_x"]     # 击杀者当时的位置坐标
                #         killer_location_y = killer_weapon_detail[weapon_name][num]["killer_y"]
                #         killer_location_z = killer_weapon_detail[weapon_name][num]["killer_z"]
                #
                #         victim_location_x = killer_weapon_detail[weapon_name][num]["victim_x"]     # 被击杀者当时的位置坐标
                #         victim_location_y = killer_weapon_detail[weapon_name][num]["victim_y"]
                #         victim_location_z = killer_weapon_detail[weapon_name][num]["victim_z"]
                #         print("\n\t\t\t第 " + str(num) + " 次击杀：")
                #         print("\t\t\t\t击杀者的位置为：\n" + "\t\t\t\t\tx : " + str(killer_location_x) + " y : " + str(killer_location_y) + " z : " + str(killer_location_z) + "\n\t\t\t\t被击杀者的位置为：\n" + "\t\t\t\t\tx : " + str(victim_location_x) + " y : " + str(victim_location_y) + " z : " + str(victim_location_z))
                print("\n\t\t游戏总时长为： " + game_Time)

            except Exception:
                pass


# def get_player_url(name):
#
#     players = pubg.players_from_names(name)   #创建玩家实例
#
#     return players.url   #返回url

def find_weapon_kills(telemetry):
    killer_weapon_total = {}      # 创建记录武器击杀次数列表
    killer_weapon_detail = {}      # 创建武器每次击杀位置信息列表
    weapon_List = ["WeapHK416", "WeapM16A4", "WeapThompson", "WeapSCAR-L", "WeapKar98k", "WeapAK47", "WeapBerylM762",
                   "WeapFNFal", "WeapSmokeBomb", "WeapSKS", "WeapGroza", "WeapUMP", "Weapvz61Skorpion", "WeapMachete",
                   "WeapSaiga12", "WeapG36C", "WeapDP12", "WeapG36C", "WeapBerreta686", "WeapVector", "WeapM24",
                   "WeapMini14", "WeapMosinNagant", "WeapMolotov", "WeapGrenade", "WeapM9", "WeapUZI", "WeapIN"]      # 创建武器名称列表

    kill_events = telemetry.filter_by("log_player_kill_v2")   # 筛选比赛击杀日志

    for kill_total in kill_events:     # 记录每种武器击杀的次数
       killer_weapon = kill_total.victim_weapon     # 击杀者使用的武器

       if killer_weapon == "":
           killer_weapon = "mauler"
       else:
           for weapon_name in weapon_List:
               if weapon_name in killer_weapon:
                   killer_weapon = weapon_name
                   break

       if killer_weapon not in killer_weapon_total:   # 初始化武器击杀次数列表
           killer_weapon_total[killer_weapon] = 1
       else:
           killer_weapon_total[killer_weapon] += 1

    for killer_weapon, total in killer_weapon_total.items():   # 初始化武器每次击杀位置信息列表
       killer_weapon_detail[killer_weapon] = {}
       killer_weapon_detail[killer_weapon]['kills_total'] = total    # 记录每种武器击杀的次数
       for num in range(1, total+1):
           killer_weapon_detail[killer_weapon][num] = {}

    for kill_total in kill_events:   # 保存每种武器击杀者和被击杀者的位置信息
       killer_weapon = kill_total.victim_weapon     # 击杀者使用的武器

       if killer_weapon == "":
           killer_weapon = "mauler"
       else:
           for weapon_name in weapon_List:
               if weapon_name in killer_weapon:
                   killer_weapon = weapon_name
                   break

       killer_location_x = 0     # 击杀者当时的位置坐标
       killer_location_y = 0
       killer_location_z = 0

       victim_location_x = round(kill_total.victim.location.x, 2)     # 被击杀者当时的位置坐标
       victim_location_y = round(kill_total.victim.location.y, 2)
       victim_location_z = round(kill_total.victim.location.z, 2)

       sum = 1  # 统计数据应保存在第几次中

       while 1:
           if killer_weapon_detail[killer_weapon][sum]:
               sum += 1
           else:
                killer_weapon_detail[killer_weapon][sum]["killer_x"] = killer_location_x
                killer_weapon_detail[killer_weapon][sum]["killer_y"] = killer_location_y
                killer_weapon_detail[killer_weapon][sum]["killer_z"] = killer_location_z
                killer_weapon_detail[killer_weapon][sum]["victim_x"] = victim_location_x
                killer_weapon_detail[killer_weapon][sum]["victim_y"] = victim_location_y
                killer_weapon_detail[killer_weapon][sum]["victim_z"] = victim_location_z
                break

    return killer_weapon_total

def get_Map_Name(telemetry):
    return telemetry.map_name()

def get_Player_Num(telemetry):
    return telemetry.num_players()

def get_Team_Num(telemetry):
    return telemetry.num_teams()

def get_Game_Mode(match):
    return match.game_mode

def get_Game_Time(match):
    time = match.duration

    mintues = time / 60
    seconds = time % 60

    result = str(round(mintues)) + " 分 " +  str(seconds) + " 秒"
    return result

# def get_Game_Attack(telemetry):
#     postion_events = telemetry.filter_by("log_player_attack")
#     attack = postion_events[30]
#     player_attack = attack.attacker
#     weapon_attack = attack.weapon
#
#     result = "\t\t发起攻击的玩家 ‘" + player_attack.name + "' 的位置在坐标在:\n\t\t\tx : " + str(round(player_attack.location.x,2)) + "  y : " + str(round(player_attack.location.y,2)) + "  z : " + str(round(player_attack.location.z,2)) + "\n\t\t\t使用的武器为： " + weapon_attack.sub_category
#     return result

def get_Vehicle_Ride(telemetry):
    vehicle_Ride_List = {}

    vehicle_leave = telemetry.filter_by("log_vehicle_leave")  # 筛选比赛击杀日志
    for player_ride in vehicle_leave:
        vehicle_Ride_List[player_ride.character.name] = round(player_ride.ride_distance, 2)

    return vehicle_Ride_List

if __name__ == "__main__": #当程序执行时
    # 调用函数
    main()
    print("获取完毕")