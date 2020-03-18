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


def calQuegong(start = 20200210, end = 20200316):
    if platform.system() == "Windows":
        path = "E:/jupyter/nCov/baiduqianxi/scp/data/city"
    else:
        path = "/data/jht/baiduqianxi/data/city"
    out_start_2020 = 20200101
    out_end_2020 = 20200124    
    
    # 爬到的城市数据列表
    cities = os.listdir(path)
    # echarts上的城市列表
    with open("./stat/shortName.json","r",encoding="utf-8") as jsonFile:
        cities_ = json.loads(jsonFile.read())
    lack = []
    cityList = []
    flag = 0
    for city in cities:
        if city in provinces:
            continue
        print("Quegong", city)
        move_in = pd.read_csv(path+"/"+city+"/historycurve/move_in.csv").sort_values(by=["date"])
        move_out= pd.read_csv(path+"/"+city+"/historycurve/move_out.csv").sort_values(by=["date"])
        
        out_2020 = move_out.loc[move_out[move_out["date"]==out_start_2020].index.tolist()[0] : move_out[move_out["date"]==out_end_2020].index.tolist()[0]]["value"].sum() - move_in.loc[move_in[move_in["date"]==out_start_2020].index.tolist()[0] : move_in[move_in["date"]==out_end_2020].index.tolist()[0]]["value"].sum()

        in_2020 = move_in.loc[move_in[move_in["date"]==start].index.tolist()[0] : move_in[move_in["date"]==end].index.tolist()[0]]["value"].cumsum() - move_out.loc[move_out[move_out["date"]==start].index.tolist()[0] : move_out[move_out["date"]==end].index.tolist()[0]]["value"].cumsum()
        # (年前净流出 - 年后净流入) / 年前净流出
        
        if out_2020 < 0:
            lack_2020 = [0 for _ in range(len(in_2020))]
        else:
            lack_2020 = ((out_2020 - in_2020) / out_2020).tolist()
            lack_2020 = [0 if i < 0 else round(i,3) for i in lack_2020]
        # if lack_2020[-1] > 1:
        #     print(out_2020)
        #     print(in_2020)
        #     print(lack_2020)
            # return
        if not flag:
            dateList = move_in.loc[move_in[move_in["date"]==start].index.tolist()[0] : move_in[move_in["date"]==end].index.tolist()[0]]["date"].values.tolist()
            dateList = [str(i)[:4]+"-"+str(i)[4:6]+"-"+str(i)[6:] for i in dateList]
            flag = 1
        # 小于0的说明不缺工了
        name = ""
        for i in cities_:
            if i in city:
                name = i
                break
        if name:
            cityList.append(name)
            lack.append(lack_2020)
    lack = np.array(lack)
    lack = lack.T.tolist()
    res = []
    for i in range(len(lack)):
        res.append({
            "date": dateList[i],
            "value" : lack[i]
        })
    with open("./stat/data/quegong_daily.json", "w", encoding="utf-8") as jsonFile:
        json.dump({"data":res,"city":cityList}, jsonFile, ensure_ascii=False)    



calQuegong()
