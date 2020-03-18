import json
import csv
import os
import sys
import pandas as pd
import numpy as np
import datetime
import platform

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

provinces = [
    '湖北省', '广东省', '浙江省', '江西省', '山东省', '河南省', '湖南省', '四川省', 
    '云南省', '山西省', '福建省', '辽宁省', '海南省', '安徽省', '贵州省', '广西壮族自治区', '宁夏回族自治区', '河北省', '江苏省', 
    '吉林省', '黑龙江省', '陕西省', '新疆维吾尔自治区', '甘肃省', '内蒙古自治区', '青海省', '西藏自治区', '香港', '澳门', '台湾省',
]


def bottomCard_fugong(day):
    if platform.system() == "Windows":
        path = "E:/jupyter/nCov/baiduqianxi/scp/data/city"
    else:
        path = "/data/jht/baiduqianxi/data/city"
    GDP_2018 = 900309.00 # 亿元
    week1_start_2020 = 20200106
    week1_end_2020 = 20200110
    week2_start_2020 = 20200113
    week2_end_2020 = 20200117
    start = 20200210
    end = day
    data = pd.read_csv("./stat/全国GDP.csv").values
    dataD = {}
    for item in data:
        if item[1] == 0:
            continue
        dataD[item[0]] = item[1]
    # 爬到的城市数据列表
    cities = os.listdir(path)
    np_data = []
    flag = 0
    for city in cities:
        if city in provinces:
            continue
        travel = pd.read_csv(path+"/"+city+"/internalflowhistory/move_in.csv").sort_values(by=["date"])
        # 年前平均活动强度
        week1_2020 = travel.loc[travel[travel["date"]==week1_start_2020].index.tolist()[0] : travel[travel["date"]==week1_end_2020].index.tolist()[0]]["value"].mean()
        week2_2020 = travel.loc[travel[travel["date"]==week2_start_2020].index.tolist()[0] : travel[travel["date"]==week2_end_2020].index.tolist()[0]]["value"].mean()
        ave = (week1_2020+week2_2020)/2
        # GDP占比
        try:
            GDP_weight = dataD[city] / GDP_2018
        except:
            continue
        # 年后至今每天的活动强度
        after_year_2020 = travel.loc[travel[travel["date"]==start].index.tolist()[0] : travel[travel["date"]==end].index.tolist()[0]]["value"].values / ave * GDP_weight
        if not flag:
            dateList = travel.loc[travel[travel["date"]==start].index.tolist()[0] : travel[travel["date"]==end].index.tolist()[0]]["date"].values.tolist()
            dateList = [str(i)[:4]+"-"+str(i)[4:6]+"-"+str(i)[6:] for i in dateList]
            flag = 1
        np_data.append(after_year_2020)
        

    np_data = np.array(np_data)
    temp = np_data.sum(axis=0).tolist()
    res_date = []
    res_value = []
    for key, value in zip(dateList, temp):
        # 去掉周末
        if datetime.datetime.strptime(key,"%Y-%m-%d").weekday() > 4:
            continue
        res_date.append(key)
        res_value.append(round(value, 3))
    with open("./stat/data/fugong_bottomCard.json","w",encoding="utf-8") as jsonFile:
        json.dump({"dateList":res_date,"value":res_value}, jsonFile, ensure_ascii=False, indent=4)

def bottomCard_quegong(day):
    if platform.system() == "Windows":
        path = "E:/jupyter/nCov/baiduqianxi/scp/data/city"
    else:
        path = "/data/jht/baiduqianxi/data/city"
    GDP_2018 = 900309.00 # 亿元
    time1 = 20200101
    time2 = 20200124
    time3 = 20200210
    time4 = day
    data = pd.read_csv("./stat/全国GDP.csv").values
    dataD = {}
    for item in data:
        if item[1] == 0:
            continue
        dataD[item[0]] = item[1]
    # 爬到的城市数据列表
    cities = os.listdir(path)
    np_data = []
    flag = 0
    for city in cities:
        if city in provinces:
            continue
        move_in = pd.read_csv(path+"/"+city+"/historycurve/move_in.csv").sort_values(by=["date"])
        move_out= pd.read_csv(path+"/"+city+"/historycurve/move_out.csv").sort_values(by=["date"])
        
        out_2020_before = move_out.loc[move_out[move_out["date"]==time1].index.tolist()[0] : move_out[move_out["date"]==time2].index.tolist()[0]]["value"].sum() - move_in.loc[move_in[move_in["date"]==time1].index.tolist()[0] : move_in[move_in["date"]==time2].index.tolist()[0]]["value"].sum()
        # 迁入是累积的
        in_2020_after = move_in.loc[move_in[move_in["date"]==time3].index.tolist()[0] : move_in[move_in["date"]==time4].index.tolist()[0]]["value"].cumsum() - move_out.loc[move_out[move_out["date"]==time3].index.tolist()[0] : move_out[move_out["date"]==time4].index.tolist()[0]]["value"].cumsum()
        # GDP占比
        try:
            GDP_weight = dataD[city] / GDP_2018
        except:
            continue
        if out_2020_before < 0:
            lack_2020 = [0 for _ in range(len(in_2020_after))]
        else:
            lack_2020 = ((out_2020_before - in_2020_after)/out_2020_before) * GDP_weight
        
        if not flag:
            dateList = move_in.loc[move_in[move_in["date"]==time3].index.tolist()[0] : move_in[move_in["date"]==time4].index.tolist()[0]]["date"].values.tolist()
            dateList = [str(i)[:4]+"-"+str(i)[4:6]+"-"+str(i)[6:] for i in dateList]
            flag = 1
        np_data.append(lack_2020)
        
    np_data = np.array(np_data)
    temp = np_data.sum(axis=0).tolist()
    res_date = []
    res_value = []
    for key, value in zip(dateList, temp):
        res_date.append(key)
        res_value.append(round(value, 3))
    print(res_value)
    with open("./stat/data/quegong_bottomCard.json","w",encoding="utf-8") as jsonFile:
        json.dump({"dateList":res_date,"value":res_value}, jsonFile, ensure_ascii=False, indent=4)

# bottomCard_fugong(20200312)
bottomCard_quegong(20200312)