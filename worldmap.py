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

def clip(value,bound=(0,1)):
    value=max(bound[0],value)
    value=min(bound[1],value)
    return value

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

nameMap = {
    "Afghanistan": "阿富汗",
    "Angola": "安哥拉",
    "Albania": "阿尔巴尼亚",
    "United Arab Emirates": "阿联酋",
    "Argentina": "阿根廷",
    "Armenia": "亚美尼亚",
    "French Southern and Antarctic Lands": "法属南半球和南极领地",
    "Australia": "澳大利亚",
    "Austria": "奥地利",
    "Azerbaijan": "阿塞拜疆",
    "Burundi": "布隆迪",
    "Belgium": "比利时",
    "Benin": "贝宁",
    "Burkina Faso": "布基纳法索",
    "Bangladesh": "孟加拉国",
    "Bulgaria": "保加利亚",
    "The Bahamas": "巴哈马",
    "Bosnia and Herzegovina": "波黑",
    "Belarus": "白俄罗斯",
    "Belize": "伯利兹",
    "Bermuda": "百慕大",
    "Bolivia": "玻利维亚",
    "Brazil": "巴西",
    "Brunei": "文莱",
    "Bhutan": "不丹",
    "Botswana": "博茨瓦纳",
    "Central African Republic": "中非共和国",
    "Canada": "加拿大",
    "Switzerland": "瑞士",
    "Chile": "智利",
    "China": "中国",
    "Ivory Coast": "象牙海岸",
    "Cameroon": "喀麦隆",
    "Democratic Republic of the Congo": "刚果（金）",
    "Republic of the Congo": "刚果（布）",
    "Colombia": "哥伦比亚",
    "Costa Rica": "哥斯达黎加",
    "Cuba": "古巴",
    "Northern Cyprus": "北塞浦路斯",
    "Cyprus": "塞浦路斯",
    "Czech Republic": "捷克",
    "Germany": "德国",
    "Djibouti": "吉布提",
    "Denmark": "丹麦",
    "Dominican Republic": "多米尼加共和国",
    "Algeria": "阿尔及利亚",
    "Ecuador": "厄瓜多尔",
    "Egypt": "埃及",
    "Eritrea": "厄立特里亚",
    "Spain": "西班牙",
    "Estonia": "爱沙尼亚",
    "Ethiopia": "埃塞俄比亚",
    "Finland": "芬兰",
    "Fiji": "斐",
    "Falkland Islands": "福克兰群岛",
    "France": "法国",
    "Gabon": "加蓬",
    "United Kingdom": "英国",
    "Georgia": "格鲁吉亚",
    "Ghana": "加纳",
    "Guinea": "几内亚",
    "Gambia": "冈比亚",
    "Guinea Bissau": "几内亚比绍",
    "Equatorial Guinea": "赤道几内亚",
    "Greece": "希腊",
    "Greenland": "格陵兰",
    "Guatemala": "危地马拉",
    "French Guiana": "法属圭亚那",
    "Guyana": "圭亚那",
    "Honduras": "洪都拉斯",
    "Croatia": "克罗地亚",
    "Haiti": "海地",
    "Hungary": "匈牙利",
    "Indonesia": "印度尼西亚",
    "India": "印度",
    "Ireland": "爱尔兰",
    "Iran": "伊朗",
    "Iraq": "伊拉克",
    "Iceland": "冰岛",
    "Israel": "以色列",
    "Italy": "意大利",
    "Jamaica": "牙买加",
    "Jordan": "约旦",
    "Japan": "日本",
    "Kazakhstan": "哈萨克斯坦",
    "Kenya": "肯尼亚",
    "Kyrgyzstan": "吉尔吉斯斯坦",
    "Cambodia": "柬埔寨",
    "South Korea": "韩国",
    "Kosovo": "科索沃",
    "Kuwait": "科威特",
    "Laos": "老挝",
    "Lebanon": "黎巴嫩",
    "Liberia": "利比里亚",
    "Libya": "利比亚",
    "Sri Lanka": "斯里兰卡",
    "Lesotho": "莱索托",
    "Lithuania": "立陶宛",
    "Luxembourg": "卢森堡",
    "Latvia": "拉脱维亚",
    "Morocco": "摩洛哥",
    "Moldova": "摩尔多瓦",
    "Madagascar": "马达加斯加",
    "Mexico": "墨西哥",
    "Macedonia": "马其顿",
    "Mali": "马里",
    "Myanmar": "缅甸",
    "Montenegro": "黑山",
    "Mongolia": "蒙古",
    "Mozambique": "莫桑比克",
    "Mauritania": "毛里塔尼亚",
    "Malawi": "马拉维",
    "Malaysia": "马来西亚",
    "Namibia": "纳米比亚",
    "New Caledonia": "新喀里多尼亚",
    "Niger": "尼日尔",
    "Nigeria": "尼日利亚",
    "Nicaragua": "尼加拉瓜",
    "Netherlands": "荷兰",
    "Norway": "挪威",
    "Nepal": "尼泊尔",
    "New Zealand": "新西兰",
    "Oman": "阿曼",
    "Pakistan": "巴基斯坦",
    "Panama": "巴拿马",
    "Peru": "秘鲁",
    "Philippines": "菲律宾",
    "Papua New Guinea": "巴布亚新几内亚",
    "Poland": "波兰",
    "Puerto Rico": "波多黎各",
    "North Korea": "朝鲜",
    "Portugal": "葡萄牙",
    "Paraguay": "巴拉圭",
    "Qatar": "卡塔尔",
    "Romania": "罗马尼亚",
    "Russia": "俄罗斯",
    "Rwanda": "卢旺达",
    "Western Sahara": "西撒哈拉",
    "Saudi Arabia": "沙特阿拉伯",
    "Sudan": "苏丹",
    "South Sudan": "南苏丹",
    "Senegal": "塞内加尔",
    "Solomon Islands": "所罗门群岛",
    "Sierra Leone": "塞拉利昂",
    "El Salvador": "萨尔瓦多",
    "Somaliland": "索马里兰",
    "Somalia": "索马里",
    "Republic of Serbia": "塞尔维亚",
    "Suriname": "苏里南",
    "Slovakia": "斯洛伐克",
    "Slovenia": "斯洛文尼亚",
    "Sweden": "瑞典",
    "Swaziland": "斯威士兰",
    "Syria": "叙利亚",
    "Chad": "乍得",
    "Togo": "多哥",
    "Thailand": "泰国",
    "Tajikistan": "塔吉克斯坦",
    "Turkmenistan": "土库曼斯坦",
    "East Timor": "东帝汶",
    "Trinidad and Tobago": "特里尼达和多巴哥",
    "Tunisia": "突尼斯",
    "Turkey": "土耳其",
    "United Republic of Tanzania": "坦桑尼亚",
    "Uganda": "乌干达",
    "Ukraine": "乌克兰",
    "Uruguay": "乌拉圭",
    "United States of America": "美国",
    "Uzbekistan": "乌兹别克斯坦",
    "Venezuela": "委内瑞拉",
    "Vietnam": "越南",
    "Vanuatu": "瓦努阿图",
    "West Bank": "西岸",
    "Yemen": "也门",
    "South Africa": "南非",
    "Zambia": "赞比亚",
    "Zimbabwe": "津巴布韦",
    "Singapore Rep.": "新加坡",
    "Dominican Rep.": "多米尼加",
    "Palestine": "巴勒斯坦",
    "Bahamas": "巴哈马",
    "Timor-Leste": "东帝汶",
    "Guinea-Bissau": "几内亚比绍",
    "Côte d'Ivoire": "科特迪瓦",
    "Siachen Glacier": "锡亚琴冰川",
    "Br. Indian Ocean Ter.": "英属印度洋领土",
    "Bosnia and Herz.": "波斯尼亚和黑塞哥维那",
    "Central African Rep.": "中非",
    "Dem. Rep. Congo": "刚果民主共和国",
    "Congo": "刚果",
    "N. Cyprus": "北塞浦路斯",
    "Czech Rep.": "捷克",
    "Eq. Guinea": "赤道几内亚",
    "Korea": "韩国",
    "Lao PDR": "老挝",
    "Dem. Rep. Korea": "朝鲜",
    "W. Sahara": "西撒哈拉",
    "S. Sudan": "南苏丹",
    "Solomon Is.": "所罗门群岛",
    "Serbia": "塞尔维亚",
    "Tanzania": "坦桑尼亚",
    "United States": "美国"
}


name = {
    'nation': '全国_不含湖北', 'hubei': '湖北_不含武汉', 'wuhan': '武汉市', 'zhejiang': '浙江省', 'guangdong': '广东省', 'henan': '河南省', 'hunan': '湖南省', 'jiangxi': '江西省', 'anhui': '安徽省', 'chongqing': '重庆市', 'jiangsu': '江苏省', 'sichuan': '四川省', 'beijing': '北京市', 'heilongjiang': '黑龙江省', 'shandong': '山东省', 'ezhou': '鄂州市', 'xiaogan': '孝感市', 'huanggang': '黄冈市', 'suizhou': '随州市', 'jingzhou': '荆州市', 'huangshi': '黄石市', 'yichang': '宜昌市', 'xiangyang': '襄阳市', 'jingmen': '荆门市', 'xianning': '咸宁市', 'shiyan': '十堰市', 'xiantao': '仙桃市', 'tianmen': '天门市', 'enshi': '恩施市', 'qianjiang': '潜江市', 'wenzhou': '温州市', 'shenzhen': '深圳市', 'guangzhou': '广州市', 'shanghai': '上海市', 'xinyang': '信阳市', 'changsha': '长沙市', 'nanchang': '南昌市', 'hangzhou': '杭州市', 'ningbo': '宁波市', 'hefei': '合肥市', 'haerbin': '哈尔滨市', 'taizhou': '台州市', 'nanyang': '南阳市', 'nationall': '全国', 'hubeiall': '湖北省', 'nation_except': '全国_不含湖北', 'hubei_except': '湖北_不含武汉', 'tianjin': '天津市', 'shanxi': '陕西省', 'hebei': '河北省', 'korea': '韩国', 'japan': '日本', 'iran': '伊朗', 'italy': '意大利', 'france': '法国', 'america': '美国', 'global':'全球_不含中国', 'belgium':'比利时', 'germany':'德国', 'netherlands':'荷兰', 'sweden':'瑞典', 'spain':'西班牙', 'england':'英国', 'greece': '希腊','switzerland': '瑞士', 'canada':'加拿大', 'philippines':'菲律宾','singapore':'新加坡', 'australia':'澳大利亚', 'malaysia':'马来西亚'
}

foreign = ['中国','韩国','日本','伊朗','意大利','法国','美国','比利时',\
'德国','荷兰','瑞典','西班牙','英国','希腊','瑞士','加拿大',\
'新加坡','澳大利亚','马来西亚','巴西','以色列','奥地利','巴西','捷克',\
'葡萄牙','芬兰','爱尔兰'#,'挪威','卢森堡',
]

feed_root='feed/'
data_root='stat/data/'

def get_name(csv):
    try:
        name_ch, _, predictDate = csv.split(".")[0].split("_")
    except:
        if csv[:7] == "全国_不含湖北":
            name_ch = "全国_不含湖北"
            predictDate = csv.split(".")[0].split("_")[-1]
        elif csv[:7] == "湖北_不含武汉":
            name_ch = "湖北_不含武汉"
            predictDate = csv.split(".")[0].split("_")[-1]
        elif csv[:7] == "全球_不含中国":
            name_ch = "全球_不含中国"
            predictDate = csv.split(".")[0].split("_")[-1]
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
        data=predict[name]
        pop=float(glob_pop[name])
        node=get_one(name_trans.get(name,name),data,geo_data,pop)
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