#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import pandas as pd
import numpy as np
import os
import datetime
import time
import csv
import re
from namemap import nameMap

predictDate='2020-03-28'

def index_max(l):
    m=0
    ret=0
    for ind in range(len(l)):
        tmp=l[ind]
        if m < tmp:
            m=tmp
            ret=ind
    return ret,m

def readjson(file):
    with open(file,'r',encoding='utf-8')as f:
        data=json.load(f)
    return data

def writejson(file,data):
    with open(file,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False)

def format_date(date,split='-'):
    date=date.split(split)
    year=date[0]
    month=date[1].lstrip('0')
    day=date[2].lstrip('0')
    return f'{month}月{day}日'

class MyWriter():
    def __init__(self,path,header,index=None):
        self.path=path
        self.header=header
        self.data=[]
        self.index=index
        if(index is not None):
            self.header.append(index)
        self.cnt=0
    def insert(self,dt):
        l=[]
        for d in dt:
            if isinstance(d,float):
                l.append(round(d,3))
            else:
                l.append(d)
        self.cnt+=1
        if self.index is not None:
            l.append(self.cnt)
        self.data.append(l)
    def save(self):
        with open(self.path,'w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f)
            writer.writerow(self.header)
            writer.writerows(self.data)




name = {
    'nation': '全国_不含湖北', 'hubei': '湖北_不含武汉', 'wuhan': '武汉市', 'zhejiang': '浙江省', 'guangdong': '广东省', 'henan': '河南省', 'hunan': '湖南省', 'jiangxi': '江西省', 'anhui': '安徽省', 'chongqing': '重庆市', 'jiangsu': '江苏省', 'sichuan': '四川省', 'beijing': '北京市', 'heilongjiang': '黑龙江省', 'shandong': '山东省', 'ezhou': '鄂州市', 'xiaogan': '孝感市', 'huanggang': '黄冈市', 'suizhou': '随州市', 'jingzhou': '荆州市', 'huangshi': '黄石市', 'yichang': '宜昌市', 'xiangyang': '襄阳市', 'jingmen': '荆门市', 'xianning': '咸宁市', 'shiyan': '十堰市', 'xiantao': '仙桃市', 'tianmen': '天门市', 'enshi': '恩施市', 'qianjiang': '潜江市', 'wenzhou': '温州市', 'shenzhen': '深圳市', 'guangzhou': '广州市', 'shanghai': '上海市', 'xinyang': '信阳市', 'changsha': '长沙市', 'nanchang': '南昌市', 'hangzhou': '杭州市', 'ningbo': '宁波市', 'hefei': '合肥市', 'haerbin': '哈尔滨市', 'taizhou': '台州市', 'nanyang': '南阳市', 'nationall': '全国', 'hubeiall': '湖北省', 'nation_except': '全国_不含湖北', 'hubei_except': '湖北_不含武汉', 'tianjin': '天津市', 'shanxi': '陕西省', 'hebei': '河北省', 'korea': '韩国', 'japan': '日本', 'iran': '伊朗', 'italy': '意大利', 'france': '法国', 'america': '美国', 'global':'全球_不含中国', 'belgium':'比利时', 'germany':'德国', 'netherlands':'荷兰', 'sweden':'瑞典', 'spain':'西班牙', 'england':'英国', 'greece': '希腊','switzerland': '瑞士', 'canada':'加拿大', 'philippines':'菲律宾','singapore':'新加坡', 'australia':'澳大利亚', 'malaysia':'马来西亚','israel':'以色列', 'luxembourg':'卢森堡', 'austria':'奥地利', 'brazil':'巴西','czech':'捷克','ireland':'爱尔兰','finland':'芬兰','portugal':'葡萄牙','norway':'挪威','denmark':'丹麦','pakistan':'巴基斯坦','thailand':'泰国', 'russia':'俄罗斯','qatar':'卡塔尔','taiwan':'台湾省','slovenia':'斯洛文尼亚','estonia':'爱沙尼亚','hongkong':'香港'
}

foreign = ['中国','韩国','日本','伊朗','意大利','法国','美国','比利时',\
'德国','荷兰','瑞典','西班牙','英国','希腊','瑞士','加拿大',\
'新加坡','澳大利亚','马来西亚','巴西','以色列','奥地利','巴西','捷克',\
'葡萄牙','芬兰','爱尔兰','挪威','丹麦','巴基斯坦','泰国','俄罗斯','卡塔尔','斯洛文尼亚','爱沙尼亚','香港'
]

feed_root='feed/'
data_root='stat/data/'

def get_name(csv):
    try:
        name_ch= csv.split(".")[0]
    except:
        if csv[:7] == "全国_不含湖北":
            name_ch = "全国_不含湖北"
        elif csv[:7] == "湖北_不含武汉":
            name_ch = "湖北_不含武汉"
        elif csv[:7] == "全球_不含中国":
            name_ch = "全球_不含中国"
        else:
            print("ERROR.")
            return (None,None,None)
    if name_ch == "全国":
        name_ch = "中国"
    if not (name_ch in foreign):
        print('error',name_ch)
        return (None,None,None)
    name_en = ""
    for key in nameMap:
        if nameMap[key] == name_ch:
            name_en = key
            break
    if len(name_en)==0:
        return (None,None,None)
    return name_ch,name_en,predictDate

def worlddata():
    # path = "E:/jupyter/nCov/accuracy/results/results0317"
    path='./results'
    fileList = os.listdir(path)
    dataList = []
    jsonData = {}
    for csv in fileList:
        print(csv)
        name_ch,name_en,predictDate=get_name(csv)
        print(predictDate," ************************")
        if name_ch is None:
            continue
        # print(name_en)
        csvData = pd.read_csv(path + "/" + csv)[ ["Date","Predict_confirm","Official_confirmed","Remain_confirm",'Dailynew_confirm'] ]
        # print(csvData['Date'][0],21-int(csvData["Date"][0].split('/')[2]))
        day = datetime.datetime.strptime(predictDate, "%Y-%m-%d")
        startDay = day + datetime.timedelta(days = -10)
        endDay = day + datetime.timedelta(days = 60)
        lastDay = day + datetime.timedelta(days = -1)
        startDayStr = datetime.datetime.strftime(startDay, "%Y/%m/%d")
        endDayStr = datetime.datetime.strftime(endDay, "%Y/%m/%d")
        lastDayStr = datetime.datetime.strftime(lastDay, "%Y/%m/%d")
        predict = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0], "Predict_confirm"].tolist()
        predict_dateList = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0], "Date"].tolist()
        actual = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==lastDayStr].index.tolist()[0], "Official_confirmed"].tolist()
        actual_dateList = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==lastDayStr].index.tolist()[0], "Date"].tolist()
        remain = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0], "Remain_confirm"].tolist()
        pred_daily_new = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0],'Dailynew_confirm'].tolist()
        if name_ch in foreign:
            dataList.append({
                "name": name_en,
                "value": actual[-1]
            })
            jsonData[name_en] = {
                "actual": {
                    "dateList": actual_dateList,
                    "value": actual
                },
                "predict": {
                    "dateList": predict_dateList,
                    "value": predict
                },
                "remain": remain,
                "daily_new":pred_daily_new,
            }
    
    with open("./stat/data/predict.json", "w", encoding="utf-8") as jsonFile:
        json.dump({
            "predict":jsonData,
            "official_confirmed": dataList,
        }, jsonFile, ensure_ascii=False, indent=4)


def world_prediction_update():
    path='./results'
    fileList = os.listdir(path)
    dataList = []
    jsonData = {}
    wt=MyWriter(feed_root+'全球疫情预测.csv',['日期','确诊预测','在治预测','新增预测','国家'],index='编号')
    for csv in fileList:
        print(csv)
        name_ch,name_en,predictDate=get_name(csv)
        if name_ch is None:
            continue
        # print(name_en)
        csvData = pd.read_csv(path + "/" + csv)[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm'] ]
        # print(csvData['Date'][0],21-int(csvData["Date"][0].split('/')[2]))
        day = datetime.datetime.strptime(predictDate, "%Y-%m-%d")
        startDay = day + datetime.timedelta(days = -10)
        endDay = day + datetime.timedelta(days = 60)
        lastDay = day + datetime.timedelta(days = -1)
        startDayStr = datetime.datetime.strftime(startDay, "%Y/%m/%d")
        endDayStr = datetime.datetime.strftime(endDay, "%Y/%m/%d")
        lastDayStr = datetime.datetime.strftime(lastDay, "%Y/%m/%d")
        predict = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0], "Predict_confirm"].tolist()
        predict_dateList = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0], "Date"].tolist()
        # actual = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==lastDayStr].index.tolist()[0], "Official_confirmed"].tolist()
        # actual_dateList = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==lastDayStr].index.tolist()[0], "Date"].tolist()
        remain = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0], "Remain_confirm"].tolist()
        pred_daily_new = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0],'Dailynew_confirm'].tolist()
        for date,predict_daily,rem,new in zip(predict_dateList,predict,remain,pred_daily_new):
            wt.insert([format_date(date,split='/'),predict_daily,rem,new,name_en])
    wt.save()

def world_current_update():
    path='./results'
    fileList = os.listdir(path)
    dataList = []
    jsonData = {}
    wt=MyWriter(feed_root+'全球疫情现状.csv',['患病人数','国家'])
    for csv in fileList:
        print(csv)
        name_ch,name_en,predictDate=get_name(csv)
        if name_ch is None:
            continue
        # print(name_en)
        csvData = pd.read_csv(path + "/" + csv)[ ["Date","Predict_confirm","Official_confirmed","Remain_confirm"] ]
        # print(csvData['Date'][0],21-int(csvData["Date"][0].split('/')[2]))
        day = datetime.datetime.strptime(predictDate, "%Y-%m-%d")
        startDay = day + datetime.timedelta(days = -10)
        endDay = day + datetime.timedelta(days = 60)
        lastDay = day + datetime.timedelta(days = -1)
        startDayStr = datetime.datetime.strftime(startDay, "%Y/%m/%d")
        endDayStr = datetime.datetime.strftime(endDay, "%Y/%m/%d")
        lastDayStr = datetime.datetime.strftime(lastDay, "%Y/%m/%d")
        # predict = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0], "Predict_confirm"].tolist()
        # predict_dateList = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0], "Date"].tolist()
        actual = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==lastDayStr].index.tolist()[0], "Official_confirmed"].tolist()
        # actual_dateList = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==lastDayStr].index.tolist()[0], "Date"].tolist()
        # remain = csvData.loc[csvData[csvData["Date"]==startDayStr].index.tolist()[0] : csvData[csvData["Date"]==endDayStr].index.tolist()[0], "Remain_confirm"].tolist()
        wt.insert([actual[-1],name_en])
    wt.save()

def future_ind(actual_date,predict_date):
    last_date=actual_date[-1]
    for ind,date in enumerate(predict_date):
        if date == last_date:
            return ind+1

def get_one(name,data,geo_data,pop):
    print(name, geo_data.keys())
    node=geo_data[name]
    prop=node['properties']
    actual=data['actual']
    predict=data['predict']
    remain=data['remain']
    dailynew=data['daily_new']
    # prop['history']=actual['value']
    prop['increase']=round(actual['value'][-1]-actual['value'][0],3)
    f_ind=future_ind(actual['dateList'],predict['dateList'])
    f_increase10=round(predict['value'][f_ind+10-1]-predict['value'][f_ind])
    prop['future_increase10']=f_increase10
    prop['future_rate10']=round(f_increase10/pop*1000000,3)
    prop['scale']=predict['value'][-1]
    ind,m=index_max(dailynew)
    prop['max_increase_date']=predict['dateList'][ind]
    prop['rate']=round(prop['increase']/pop*1000000,3)
    prop['current']=actual['value'][-1]
    node['properties']=prop
    del node['id']
    return node

def world_map_update():
    glob_pop=readjson(data_root+'worldPopulation.json')
    name_trans={'Singapore Rep.':'Singapore',
    "United States":"United States of America",
    "Korea":"South Korea"}
    predict=readjson(data_root+'predict.json')
    predict=predict['predict']
    country_geojson=readjson(data_root+'country_geojson.json')['features']
    geo_data={}
    for item in country_geojson:
        geo_data[item['properties']['name']]=item
    features=[]
    for name in predict:
        name=name_trans.get(name,name)
        data=predict[name]
        pop=float(glob_pop[name])
        if name == "United States of America":
            name = "USA"
        if name == "United Kingdom":
            name = "UK"
        if name == "Czech Republic":
            name = "Czech Rep."
        node=get_one(name,data,geo_data,pop)
        features.append(node)
    geojson={"type":"FeatureCollection","features":features}
    writejson(feed_root+"world_pred.json",geojson)
        

def world_data_main():
    worlddata()
    world_map_update()
    world_current_update()
    world_prediction_update()

if __name__=='__main__':
    world_data_main()