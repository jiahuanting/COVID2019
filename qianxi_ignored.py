"""
复工率指数 = 最近一周每天城内出行强度 / 年前2、3周城内平均每天出行强度 ### 需要用到internalflowhistory
城市相对复工率指数 = 今年的 / 去年的
缺工规模指数 = 年前3周的人口净迁出规模指数 - 年后3周的人口净迁入规模指数
缺工率指数 = 缺工规模指数 / 常住人口数
去年除夕2.4号 春节2.5号 年前第三周和二周分别是1.14-1.18 1.21-1.25年后第一周是2.25-3.1
"""

import json
import csv
import os
import sys
import pandas as pd
import numpy as np
import datetime


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

provinces = [
    '湖北省', '广东省', '浙江省', '江西省', '山东省', '河南省', '湖南省', '四川省', 
    '云南省', '山西省', '福建省', '辽宁省', '海南省', '安徽省', '贵州省', '广西壮族自治区', '宁夏回族自治区', '河北省', '江苏省', 
    '吉林省', '黑龙江省', '陕西省', '新疆维吾尔自治区', '甘肃省', '内蒙古自治区', '青海省', '西藏自治区', '香港', '澳门', '台湾省',
]


def merge():
    with open("./stat/data/fugong_daily.json","r",encoding="utf-8") as jsonFile:
        fugong_daily = json.loads(jsonFile.read())
    with open("./stat/data/quegong_daily.json","r",encoding="utf-8") as jsonFile:
        quegong_daily = json.loads(jsonFile.read())
    with open("./stat/data/fugong_bottomCard.json", "r", encoding="utf-8") as jsonFile:
        fugong_bottomCard = json.loads(jsonFile.read())
    with open("./stat/data/quegong_bottomCard.json", "r", encoding="utf-8") as jsonFile:
        quegong_bottomCard = json.loads(jsonFile.read())
    with open("./stat/data/sideCard.json", "r", encoding="utf-8") as jsonFile:
        sideCard = json.loads(jsonFile.read())
    
    with open("./stat/data/dataR.json","w",encoding="utf-8") as jsonFile:
        json.dump({
            "fugong_daily": fugong_daily, 
            "quegong_daily": quegong_daily, 
            "fugong_bottomCard": fugong_bottomCard,
            "quegong_bottomCard": quegong_bottomCard, 
            "sideCard": sideCard
        }, jsonFile, ensure_ascii=False)


def changeName():
    with open("./stat/shortName.json","r",encoding="utf-8") as jsonFile:
        cities_ = json.loads(jsonFile.read())
    data = pd.read_csv("./stat/全国GDP.csv").values
    GDP = {}
    check = 0
    for item in data:
        city = item[0]
        for i in cities_:
            if i in city:
                GDP[i] = item[1]
                check = check + item[1]
                break
    print(check)
    with open("./stat/GDP.json","w",encoding="utf-8") as jsonFile:
        json.dump(GDP, jsonFile, ensure_ascii=False, indent=4)


merge()
