# -*- coding = utf-8 -*-
# @Time : 2021/7/8 23:12
# @Author :　James
# @File : Get_data.py
# @Software: PyCharm

from chicken_dinner.pubgapi import PUBGCore,PUBG, pubg
import csv
import os
import sys
import configparser
import pandas as pd
from time import sleep

dirPath=''
if getattr(sys, 'frozen', False):
    dirPath = os.path.dirname(sys.executable)
elif __file__:
    dirPath = os.path.dirname(os.path.abspath(__file__))

localPath=dirPath
dirPath = os.path.dirname(dirPath)

cf = configparser.ConfigParser()
cf.read(os.path.join(dirPath, "config.ini"))

# 创建PUBG实例，api_key(API秘钥），shard（对服务器进行获取）
api_key = cf.get("spider","key")
pubg = PUBG(api_key=api_key, shard="steam")

# 统计武器的两种地图名字信息
weapon_kills_total = {"Erangel (Remastered)", "Miramar"}
# 分别保存两个地图武器总击杀数字典
erangel_weapon_kills = {}
miramar_weapon_kills = {}


def main():
    # 建立用户文件路径
    path=os.path.join(dirPath,'username.csv')

    # 读取用户信息文件并存储在列表中
    with open(path, 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    global_sum = 0
    sum_total = 0
    len_death_detail = 0
    len_player_total = 0
    global_total = 0

    # 读取列表中的用户信息
    for row_player in rows:
        if sum_total <= 5:
            # 创建所需要获取的地图列表
            map_list = ["Erangel (Remastered)", "Miramar"]
            # 吃鸡玩家具体信息
            winner_detail_total = []
            # 非吃鸡玩家具体信息
            unwinner_detail_total = []
            # 死亡时间小于3分钟的玩家信息
            death_early_player_total = []

            # 总玩家信息汇总表
            player_detail_finnal_total = []
            # 统计三分钟内死亡玩家的各类信息
            death_player_total_detail = []
            name = row_player[1]

            try:
                # 创建玩家实例
                players = pubg.players_from_names(name)
                player = players[0]
            except Exception as e:
                print(e)
                sleep(60)
                continue

            for i in range(10):
                try:
                    if i == 0:
                        print("玩家 '" + player.name + "' 的近期参加的比赛所有情况： ")

                    # 获取玩家近期比赛ID
                    match = pubg.match(player.match_ids[i])
                    # 创建一局比赛中的所有日志集合实例
                    telemetry = match.get_telemetry()
                    # 筛选只获取海岛和沙漠地图信息
                    map_Name = get_Map_Name(telemetry)

                    if map_Name not in map_list:
                        continue

                    # 保存比赛人数信息
                    player_Num = get_Player_Num(telemetry)
                    # 保存比赛队伍信息
                    team_Num = get_Team_Num(telemetry)
                    # 保存比赛模式信息
                    game_Mode = get_Game_Mode(match)
                    # 保存比赛持续时间信息
                    game_Time = get_Game_Time(match)
                    # 保存玩家是否吃鸡信息
                    player_result = get_Player_Name(match)
                    # 保存玩家所有个人信息
                    player_game_detail = get_player_details(match)
                    # 保存武器击杀数信息
                    killer_weapon_detail = find_weapon_kills(telemetry)
                    # 保存在毒圈内死亡的位置信息
                    death_detail = find_death_total(telemetry)
                    # 整合玩家吃鸡时小队人数、击杀数、助攻数、乘车距离和存活时长信息
                    winner_detail = together_winner_detail(player_result, player_game_detail)
                    # 整合玩家没有吃鸡时小队人数、击杀数、助攻数、乘车距离和存活时长信息
                    unwinner_detail = together_unwinner_detail(player_result, player_game_detail)

                    # 保存所有玩家个人最终信息
                    for player_game_name in player_game_detail:
                        player_detail_finnal_total.append([map_Name, player_game_name,
                                                           player_game_detail[player_game_name]["win_place"],
                                                           player_game_detail[player_game_name]["kills"],
                                                           player_game_detail[player_game_name]["assists"],
                                                           player_game_detail[player_game_name]["damage_dealt"],
                                                           player_game_detail[player_game_name]["ride_distance"],
                                                           player_game_detail[player_game_name]["walk_distance"]])

                    # 保存所有死亡玩家的最终信息
                    for player_death_name in unwinner_detail:
                        current_detail = [map_Name]
                        if unwinner_detail[player_death_name]["time_survived"] <= 180:
                            for player_death_place in player_game_detail:
                                if player_death_place == player_death_name:
                                    current_detail.append(player_death_name)
                                    current_detail.append(player_game_detail[player_death_place]["win_place"])
                            for player_death_detail_current in death_detail:
                                if player_death_detail_current[0] == player_death_name:
                                    current_detail.append(player_death_detail_current[1])
                                    current_detail.append(player_death_detail_current[2])
                                    current_detail.append(unwinner_detail[player_death_name]["time_survived"])
                            death_player_total_detail.append(current_detail)

                    # 创建保存存活时间小于3分钟的玩家列表
                    death_early_name = []
                    # 保存存活时间小于3分钟的玩家名
                    for death_early_detail in unwinner_detail:
                        if unwinner_detail[death_early_detail]["time_survived"] <= 180:
                            death_early_name.append(
                                [death_early_detail, unwinner_detail[death_early_detail]["time_survived"]])
                    # 保存存活时间小于3分钟的玩家的位置信息
                    for detail in death_early_name:
                        for location in death_detail:
                            if location[0] == detail[0]:
                                death_early_player_total.append(
                                    [map_Name, location[0], location[1], location[2], detail[1]])

                    # 保存海岛地图武器击杀数信息
                    if map_Name == "Erangel (Remastered)":
                        for kill_name, number in killer_weapon_detail.items():  # 记录每种武器击杀的次数
                            # print(kill_name, " 击杀数为： ", number)
                            if kill_name in erangel_weapon_kills:
                                erangel_weapon_kills[kill_name] += number
                            else:
                                erangel_weapon_kills[kill_name] = number
                    # 保存沙漠地图武器击杀数信息`
                    elif map_Name == "Miramar":
                        for kill_name, number in killer_weapon_detail.items():  # 记录每种武器击杀的次数
                            # print(kill_name, " 击杀数为： ", number)
                            if kill_name in miramar_weapon_kills:
                                miramar_weapon_kills[kill_name] += number
                            else:
                                miramar_weapon_kills[kill_name] = number

                    sum_total += 1
                    global_sum += 1

                    print("第 " + str(i + 1) + " 场游戏中 : ")
                    print("\t\t地图为： " + map_Name)
                    print("\t\t游戏模式为： " + game_Mode)
                    print("\t\t玩家人数为： " + str(player_Num))
                    print("\t\t队伍数量为： " + str(team_Num))
                    print("\n\t\t游戏总时长为： " + game_Time)
                    print("*********** 第", global_sum, "次获取成功 ***********")

                except Exception:
                    pass

        else:
            # 对两个地图中武器击杀数的信息进行保存和和建表
            # 保存两个地图名字列表
            erangel_weapon_name = []
            erangel_kills_total = []
            # 保存两个地图中武器击杀总数列表
            miramar_weapon_name = []
            miramar_kills_total = []
            # 保存地图中武器总击杀数
            for weapon_name, number in erangel_weapon_kills.items():
                erangel_weapon_name.append(weapon_name)
                erangel_kills_total.append(number)
            for weapon_name, number in miramar_weapon_kills.items():
                miramar_weapon_name.append(weapon_name)
                miramar_kills_total.append(number)
            # 对两个海岛地图的武器击杀数进行规格化处理
            erangel_weapon = pd.Series(erangel_kills_total, index=erangel_weapon_name)
            miramar_weapon = pd.Series(miramar_kills_total, index=miramar_weapon_name)
            # 建立保存两个地图的图表位置
            erangel_path = os.path.join(localPath, 'erangel_weapon_1.csv')
            miramar_path = os.path.join(localPath, 'miramar_weapon_1.csv')
            # 建立两个地图的csv表
            df1 = pd.DataFrame({'Erangel (Remastered)': erangel_weapon})
            df2 = pd.DataFrame({'Miramar': miramar_weapon})
            # 保存两个地图的csv表
            df1.to_csv(erangel_path, encoding='utf8')
            df2.to_csv(miramar_path, encoding='utf8')
            # 对两个地图中武器击杀数的信息进行保存和和建表


            # 对所有存活时间少于三分钟的玩家进行保存和建表
            # 保存存活时长小于三分钟的玩家地图
            early_death_map = []
            # 保存存活时长小于三分钟的玩家姓名
            early_death_name = []
            # 保存存活时长小于三分钟的玩家位置 "x" 信息
            early_death_location_x = []
            # 保存存活时长小于三分钟的玩家位置 "y" 信息
            early_death_location_y = []
            # 保存存活时长小于三分钟的玩家存活时长信息
            early_death_time = []
            # 分别保存存活时间小于三分钟的玩家的各类信息
            for early_death in death_early_player_total:
                # 保存存活时间小于三分钟的玩家姓名
                early_death_map.append(early_death[0])
                # 保存存活时间小于三分钟的玩家姓名
                early_death_name.append(early_death[1])
                # 保存存活时间小于三分钟的 "x" 坐标
                early_death_location_x.append(early_death[2])
                # 保存存活时间小于三分钟的 "y" 坐标
                early_death_location_y.append(early_death[3])
                # 保存存活时间小于三分钟的存活时间
                early_death_time.append(early_death[4])
            # 建立保存存活时间小于三分钟的玩家信息csv表路径
            early_death_path = os.path.join(localPath, 'early_death_detail_1.csv')
            # 建立存活时间小于三分钟的玩家信息csv表
            df5 = pd.DataFrame({'Map': early_death_map, 'Name': early_death_name, "location_x": early_death_location_x,
                                "location_y": early_death_location_y, "time_survive": early_death_time})
            # 保存存活时间小于三分钟的玩家信息csv表
            df5.to_csv(early_death_path, mode='a', encoding='utf-8')
            # 完成对所有存活时间少于三分种的玩家信息的保存和建表


            # 对所有玩家的最终信息进行建表和保存
            # 保存最终玩家地图信息
            finnal_player_map = []
            # 保存最终玩家姓名信息
            finnal_player_name = []
            # 保存最终玩家队伍排名信息
            finnal_player_win_place = []
            # 保存最终玩家击杀信息
            finnal_player_kills = []
            # 保存最终玩家助攻数信息
            finnal_player_assists = []
            # 保存最终玩家造成伤害信息
            finnal_player_damage = []
            # 保存最终玩家载具距离信息
            finnal_player_ride_distance = []
            # 保存最终玩家步行距离信息
            finnal_player_walk_distance = []
            # 分别保存玩家的最终汇总信息
            for finnal_player in player_detail_finnal_total:
                # 保存玩家最终信息的地图信息
                finnal_player_map.append(finnal_player[0])
                # 保存玩家最终信息的姓名信息
                finnal_player_name.append(finnal_player[1])
                # 保存玩家最终信息的队伍排名信息
                finnal_player_win_place.append(finnal_player[2])
                # 保存玩家最终信息的击杀数信息
                finnal_player_kills.append(finnal_player[3])
                # 保存玩家最终信息的助攻数信息
                finnal_player_assists.append(finnal_player[4])
                # 保存玩家最终信息的造成伤害信息
                finnal_player_damage.append(finnal_player[5])
                # 保存玩家最终信息的载具距离信息
                finnal_player_ride_distance.append(finnal_player[6])
                # 保存玩家最终信息的步行距离信息
                finnal_player_walk_distance.append(finnal_player[7])
            # 建立保存玩家最终信息csv表的路径
            finnal_player_detail_path = os.path.join(localPath, 'finnal_player_detail_1.csv')
            # 建立保存玩家最终信息csv表
            df6 = pd.DataFrame({'Map': finnal_player_map, 'Name': finnal_player_name, 'win_place': finnal_player_win_place,
                                'kills': finnal_player_kills, 'assists': finnal_player_assists,
                                'damage_dealt': finnal_player_damage, 'ride_distance': finnal_player_ride_distance,
                                'walk_distane': finnal_player_walk_distance})
            # 保存玩家最终信息csv表
            df6.index += len_player_total
            df6.to_csv(finnal_player_detail_path, mode='a', header=False, encoding='utf-8')
            len_player_total += len(finnal_player_name)
            print("已保存的玩家所有个人信息数量为： " + str(len_player_total))
            # 完成对所有玩家的最终信息进行建表和保存


            # 对所有死亡玩家的最终位置信息进行建表和保存
            # 保存死亡玩家地图信息
            finnal_death_player_map = []
            # 保存死亡玩家姓名信息
            finnal_death_player_name = []
            # 保存死亡玩家队伍排名信息
            finnal_death_player_win_place = []
            # 保存死亡玩家的 “x” 坐标
            finnal_death_player_location_x = []
            # 保存死亡玩家的 “y” 坐标
            finnal_death_player_location_y = []
            # 保存死亡玩家存活时间
            finnal_death_player_time = []
            # 分别保存死亡玩家的最终汇总信息
            for finnal_death_player in death_player_total_detail:
                # 保存死亡玩家最终信息的地图信息
                finnal_death_player_map.append(finnal_death_player[0])
                # 保存死亡玩家最终信息的姓名信息
                finnal_death_player_name.append(finnal_death_player[1])
                # 保存死亡玩家最终信息的队伍排名信息
                finnal_death_player_win_place.append(finnal_death_player[2])
                # 保存死亡玩家最终 “x” 坐标信息
                finnal_death_player_location_x.append(finnal_death_player[3])
                # 保存死亡玩家最终 “y” 坐标信息
                finnal_death_player_location_y.append(finnal_death_player[4])
                # 保存死亡玩家最终存活时间信息
                finnal_death_player_time.append(finnal_death_player[5])
            # 建立保存死亡玩家最终信息csv表的路径
            death_player_detail_path = "D:\\爬虫\\death_player_detail.csv"
            # 建立保存死亡玩家最终信息csv表
            df7 = pd.DataFrame({'Map': finnal_death_player_map, 'Name': finnal_death_player_name,
                                'win_place': finnal_death_player_win_place,
                                'location_x': finnal_death_player_location_x, 'location_y': finnal_death_player_location_y,
                                'time_survived': finnal_death_player_time})
            # 保存死亡玩家最终信息csv表
            df7.index += len_death_detail
            df7.to_csv(death_player_detail_path, mode='a', header=False, encoding='utf-8')
            len_death_detail += len(finnal_death_player_name)
            print("已保存的所有死亡玩家信息数量为： " + str(len_death_detail))
            # 完成对所有死亡玩家的最终信息进行建表和保存

            sum_total = 0
            global_total += 1
            print("\n*************** 第 " + str(global_total) + "次保存数据成功 ***************\n")


def together_unwinner_detail(player_total, play_details):
    # 建立非吃鸡玩家信息列表
    unwinner_detail = {}

    for player_name in player_total:
        if player_total[player_name] == True:
           continue
        else:
            unwinner_detail[player_name] = {}
            unwinner_detail[player_name]["team_people"] = play_details[player_name]["team_people"]
            unwinner_detail[player_name]["kills"] = play_details[player_name]["kills"]
            unwinner_detail[player_name]["assists"] = play_details[player_name]["assists"]
            unwinner_detail[player_name]["ride_distance"] = play_details[player_name]["ride_distance"]
            unwinner_detail[player_name]["time_survived"] = play_details[player_name]["time_survived"]

    return unwinner_detail

def together_winner_detail(player_total, play_details):
    # 建立吃鸡玩家信息列表
    winner_detail = {}

    for player_name in player_total:
        if player_total[player_name] == False:
           continue
        else:
            winner_detail[player_name] = {}
            winner_detail[player_name]["team_people"] = play_details[player_name]["team_people"]
            winner_detail[player_name]["kills"] = play_details[player_name]["kills"]
            winner_detail[player_name]["assists"] = play_details[player_name]["assists"]
            winner_detail[player_name]["ride_distance"] = play_details[player_name]["ride_distance"]
            winner_detail[player_name]["time_survived"] = play_details[player_name]["time_survived"]

    return winner_detail

def get_player_details(match):
    # 创建包含玩家击杀数和助攻数的字典
    player_details = {}

    # 获取比赛玩家花名册
    rosters = match.rosters

    for roster in rosters:
        roster_participants = roster.participants
        team_number = len(roster_participants)
        for participants in roster_participants:
            player_details[participants.name] = {}
            player_details[participants.name]["team_people"] = team_number
            player_details[participants.name]["kills"] = participants.stats["kills"]
            player_details[participants.name]["assists"] = participants.stats["assists"]
            player_details[participants.name]["walk_distance"] = participants.stats["walk_distance"]
            player_details[participants.name]["ride_distance"] = participants.stats["ride_distance"]
            player_details[participants.name]["time_survived"] = participants.stats["time_survived"]
            player_details[participants.name]["win_place"] = participants.stats["win_place"]
            player_details[participants.name]["damage_dealt"] = participants.stats["damage_dealt"]

    return player_details

def find_death_total(telemetry):
    # 创建保存死亡地点信息
    death_loaction_total = []
    # 获取击杀信息日志
    death_events = telemetry.filter_by("log_player_kill_v2")

    for death_event in death_events:
        # 被击杀者的名字
        death_name = death_event.victim.name
        # 被击杀者当时的位置坐标
        death_location_x = round(death_event.victim.location.x, 2)
        death_location_y = round(death_event.victim.location.y, 2)
        # 被击杀者是否在毒圈内死亡
        death_reason = death_event.victim.is_in_blue_zone

        # 将在毒圈内死亡的玩家位置信息保存
        death_loaction_total.append([death_name, death_location_x, death_location_y, death_reason])

    return death_loaction_total


def find_weapon_kills(telemetry):
    # 创建记录武器击杀次数列表
    killer_weapon_total = {}

    # 创建武器每次击杀位置信息列表
    killer_weapon_detail = {}

    # 创建武器名称列表
    weapon_List = ["WeapHK416", "WeapM16A4", "WeapThompson", "WeapSCAR-L", "WeapKar98k", "WeapAK47", "WeapBerylM762",
                   "WeapFNFal", "WeapSmokeBomb", "WeapSKS", "WeapGroza", "WeapUMP", "Weapvz61Skorpion", "WeapMachete",
                   "WeapSaiga12", "WeapG36C", "WeapDP12", "WeapG36C", "WeapBerreta686", "WeapVector", "WeapM24",
                   "WeapMini14", "WeapMosinNagant", "WeapMolotov", "WeapGrenade", "WeapM9", "WeapUZI", "WeapIN", "WeapVSS",
                   "WeapWinchester", "WeapMk14", "WeapFlashBang", "WeapBizonPP19", "WeapBizonPP19", "WeapAUG", "WeapAWM",
                   "WeapM1911", "WeapMk47Mutant", "WeapDP28", "WeapWin94", "WeapCrossbow", "WeapNagantM1895", "WeapC4",
                   "WeapSickle", "WeapNagantM1895"]

    # 筛选比赛击杀日志
    kill_events = telemetry.filter_by("log_player_kill_v2")

    # 记录每种武器击杀的次数
    for kill_total in kill_events:
        # 击杀者使用的武器
        killer_weapon = kill_total.victim_weapon
        # print(kill_total.victim.keys())
        if killer_weapon == "":
            killer_weapon = "mauler"
        else:
            for weapon_name in weapon_List:
                if weapon_name in killer_weapon:
                    killer_weapon = weapon_name
                    break

        # 初始化武器击杀次数列表
        if killer_weapon not in killer_weapon_total:
            killer_weapon_total[killer_weapon] = 1
        else:
            killer_weapon_total[killer_weapon] += 1

    # 初始化武器每次击杀位置信息列表
    for killer_weapon, total in killer_weapon_total.items():
        killer_weapon_detail[killer_weapon] = {}

        killer_weapon_detail[killer_weapon]['kills_total'] = total  # 记录每种武器击杀的次数

        for num in range(1, total + 1):
            killer_weapon_detail[killer_weapon][num] = {}

    # 保存每种武器击杀者和被击杀者的位置信息
    for kill_total in kill_events:
       killer_weapon = kill_total.victim_weapon     # 击杀者使用的武器

       if killer_weapon == "":
           killer_weapon = "mauler"
       else:
           for weapon_name in weapon_List:
               if weapon_name in killer_weapon:
                   killer_weapon = weapon_name
                   break

       # 击杀者当时的位置坐标
       killer_location_x = 0
       killer_location_y = 0
       killer_location_z = 0

       # 被击杀者当时的位置坐标
       victim_location_x = round(kill_total.victim.location.x, 2)
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

def get_Player_Name(match):
    # 建立玩家是否吃鸡列表
    Player_detail = {}

    # 获取所有队伍信息
    rosters = match.rosters

    for roster in rosters:
        for name in roster.player_names:
            Player_detail[name] = roster.won

    return Player_detail

def get_Game_Time(match):
    # 获取游戏时长
    time = match.duration

    # 对游戏时长进行转换
    mintues = time / 60
    seconds = time % 60

    result = str(round(mintues)) + " 分 " +  str(seconds) + " 秒"

    return result

if __name__ == "__main__": #当程序执行时
    # 调用函数
    main()
    print("\n\t获取完毕")