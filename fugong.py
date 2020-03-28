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


def calFugong(start = 20200210, end = 20200316):
    if platform.system() == "Windows":
        path = "E:/jupyter/nCov/baiduqianxi/scp/data/city"
    else:
        path = "/data/jht/baiduqianxi/data/city"
    # 年前第二三周平均活动强度
    week1_start_2020 = 20200106
    week1_end_2020 = 20200110
    week2_start_2020 = 20200113
    week2_end_2020 = 20200117
    # 爬到的城市数据列表
    cities = os.listdir(path)
    # echarts上的城市列表
    with open("./stat/shortName.json","r",encoding="utf-8") as jsonFile:
        cities_ = json.loads(jsonFile.read())
    resumption = []
    cityList = []
    flag = 0
    for city in cities:
        if city in provinces:
            continue
        print("Fugong", city)
        travel = pd.read_csv(path+"/"+city+"/internalflowhistory/move_in.csv").sort_values(by=["date"])
        
        week1_2020 = travel.loc[travel[travel["date"]==week1_start_2020].index.tolist()[0] : travel[travel["date"]==week1_end_2020].index.tolist()[0]]["value"].mean()
        week2_2020 = travel.loc[travel[travel["date"]==week2_start_2020].index.tolist()[0] : travel[travel["date"]==week2_end_2020].index.tolist()[0]]["value"].mean()
        week3_2020 = travel.loc[travel[travel["date"]==start].index.tolist()[0] : travel[travel["date"]==end].index.tolist()[0]]["value"] # 出行强度列表
        
        work_resumption_2020 = (week3_2020 / ((week1_2020+week2_2020)/2)).tolist()
        work_resumption_2020 = [ 1.0 if i > 1 else round(i, 3) for i in work_resumption_2020 ]
        if not flag:
            dateList = travel.loc[travel[travel["date"]==start].index.tolist()[0] : travel[travel["date"]==end].index.tolist()[0]]["date"].values.tolist()
            dateList = [str(i)[:4]+"-"+str(i)[4:6]+"-"+str(i)[6:] for i in dateList]
            flag = 1
        name = ""
        for i in cities_:
            if i in city:
                name = city
                break
        if name:
            cityList.append(name)
            resumption.append(work_resumption_2020)

    resumption = np.array(resumption)
    resumption = resumption.T.tolist()
    res = []
    for i in range(len(resumption)):
        res.append({
            "date": dateList[i],
            "value": resumption[i]
        })
    with open("./stat/data/fugong_daily.json", "w", encoding="utf-8") as jsonFile:
        json.dump({"data":res,"city":cityList}, jsonFile, ensure_ascii=False)

if __name__=='__main__':
    calFugong()
