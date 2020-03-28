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


def sideCard(day):
    if platform.system() == "Windows":
        path = "E:/jupyter/nCov/baiduqianxi/scp/data/city"
    else:
        path = "/data/jht/baiduqianxi/data/city"
    with open("./stat/shortName.json","r",encoding="utf-8") as jsonFile:
        cities_ = json.loads(jsonFile.read())
    cityList = os.listdir(path)
    netflow = []
    for city in cityList:
        movein = pd.read_csv(path+"/"+city+"/historycurve/move_in.csv").sort_values(by=["date"])
        moveout= pd.read_csv(path+"/"+city+"/historycurve/move_out.csv").sort_values(by=["date"])

        netinflow = movein.loc[movein[movein["date"]==20200210].index.tolist()[0] : movein[movein["date"]==day].index.tolist()[0]]["value"].sum() - moveout.loc[moveout[moveout["date"]==20200210].index.tolist()[0] : moveout[moveout["date"]==day].index.tolist()[0]]["value"].sum()
        name = ""
        for i in cities_:
            if i in city:
                name = i
        if name:
            netflow.append([name, round(netinflow, 3)])

    dfin = pd.DataFrame(netflow, columns=["city","value"]).sort_values(by=["value"],ascending=False).head(10).values.tolist()
    dfout = pd.DataFrame(netflow, columns=["city","value"]).sort_values(by=["value"],ascending=True).head(10).values.tolist()
    dfin.reverse()
    dfout.reverse()
    netin = [{"city":item[0],"value":item[1]} for item in dfin]
    netout = [{"city":item[0],"value":-item[1]} for item in dfout]
    with open("./stat/data/sideCard.json", "w", encoding="utf-8") as jsonFile:
        json.dump({"in":netin, "out":netout}, jsonFile, ensure_ascii=False)

if __name__=='__main__':
    sideCard(20200316)
