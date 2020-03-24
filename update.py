#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bottomCard import bottomCard_fugong,bottomCard_quegong
from fugong import calFugong
from quegong import calQuegong
from sideCard import sideCard
# from worldmap import world_data_main
from time import time,strftime,localtime
import csv
import json
import re
import pandas as pd

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

def format_date(date):
    date=date.split('-')
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
        with open(self.path,'w',newline='',encoding='gbk') as f:
            writer=csv.writer(f)
            writer.writerow(self.header)
            writer.writerows(self.data)

provinces = [
    '湖北省', '广东省', '浙江省', '江西省', '山东省', '河南省', '湖南省', '四川省', 
    '云南省', '山西省', '福建省', '辽宁省', '海南省', '安徽省', '贵州省', '广西壮族自治区', '宁夏回族自治区', '河北省', '江苏省', 
    '吉林省', '黑龙江省', '陕西省', '新疆维吾尔自治区', '甘肃省', '内蒙古自治区', '青海省', '西藏自治区', '香港', '澳门', '台湾省',
]

feed_root='feed/'
data_root='stat/data/'
def left_header():
    wt=MyWriter(feed_root+'left_header.csv',['恢复指数','复工指数','缺工指数'])
    fugong = readjson(data_root+'fugong_bottomCard.json')
    quegong= readjson(data_root+'quegong_bottomCard.json')
    newf=clip(fugong['value'][-1])
    newq=clip(quegong['value'][-1])
    recov=(newf+(1-newq))/2
    wt.insert([recov,newf,newq])
    wt.save()

def btm_curv():
    wt=MyWriter(feed_root+'btm.csv',['日期','恢复指数','复工指数','缺工指数'])
    fugong = readjson(data_root+'fugong_bottomCard.json')
    quegong= readjson(data_root+'quegong_bottomCard.json')
    date=fugong['dateList']
    for ind,d in enumerate(date):
        f=clip(fugong['value'][ind])
        q=clip(quegong['value'][ind])
        r=(f+(1-q))/2
        wt.insert([d,r,f,q])
    wt.save()


def cleantxt(raw,shortName):
    fil = re.compile(u'[^0-9a-zA-Z\u4e00-\u9fa5.，,。？“”]+', re.UNICODE)
    name= fil.sub(' ', raw).strip()
    for c in shortName:
        if c in name:
            name=c
            break
    return name

def get_shortname(tmp,shortName):
    name=tmp
    for c in shortName:
        if c in tmp:
            name=c
            break
    return name

def left_table():
    with open("./stat/shortName.json","r",encoding="utf-8") as jsonFile:
        cities_ = json.loads(jsonFile.read())

    fugong = readjson(data_root+'fugong_daily.json')
    quegong = readjson(data_root+'quegong_daily.json')['data']
    cities=fugong['city']
    fugong=fugong['data']
    
    tmp=readjson('stat/cities_codes.json')
    city2code=tmp['city2code']
    code2province=tmp['code2province']
    
    city2gdp={}
    with open('stat/全国GDP.csv','r',encoding='utf-8') as f:
        f_csv=csv.reader(f)
        for ind,row in enumerate(f_csv):
            if(ind==0):
                continue
            cname=cleantxt(row[0],cities_)
            city2gdp[cname]=float(row[1])
    
    province2gdp={}
    for ind,c in enumerate(cities):
        if(c in provinces):
            continue
        c=get_shortname(c,cities_)
        gdp=city2gdp[c]
        code=city2code[c][0:2]
        sf=get_shortname(code2province[code],cities_)
        if(city2code[c][2:]=='0000'):
            print(c,city2code[c],sf)
        province2gdp[sf]=province2gdp.get(sf,0)+gdp

    sf2fugong={}
    sf2quegong={}
    for ind,c in enumerate(cities):
        c=get_shortname(c,cities_)
        gdp=city2gdp[c]
        code=city2code[c][0:2]
        sf=get_shortname(code2province[code],cities_)
        sgdp=province2gdp[sf]
        f=clip(fugong[-1]['value'][ind])
        q=clip(quegong[-1]['value'][ind])
        sf2fugong[sf]=sf2fugong.get(sf,0)+f*gdp/sgdp
        sf2quegong[sf]=sf2quegong.get(sf,0)+q*gdp/sgdp

    wt=MyWriter(feed_root+'省份复工指数.csv',['省份','GDP','复工指数','缺工指数','恢复指数'])
    def all_up():
        fugong = readjson(data_root+'fugong_bottomCard.json')
        quegong= readjson(data_root+'quegong_bottomCard.json')
        newf=clip(fugong['value'][-1])
        newq=clip(quegong['value'][-1])
        recov=(newf+(1-newq))/2
        return ['全国',900309.00,newf,newq,recov]
    wt.insert(all_up())
    for sf,gdp in province2gdp.items():
        f=sf2fugong[sf]
        q=sf2quegong[sf]
        r=(f+(1-q))/2
        wt.insert([sf,gdp,f,q,r])
    wt.save()

def right_bars():
    sideCard=readjson(data_root+'sideCard.json')
    trans={'in':'迁入指数','out':'迁出指数'}
    for phase in ['in','out']:
        wt=MyWriter(feed_root+trans[phase][0:2]+'.csv',['城市',trans[phase]])
        for item in sideCard[phase]:
            c=item['city']
            v=item['value']
            wt.insert([c,v])
        wt.save()

def assert_date():
    fugong_daily = readjson(data_root+'fugong_daily.json')['data']
    quegong_daily = readjson(data_root+'quegong_daily.json')['data']
    fugong_all = readjson(data_root+'fugong_bottomCard.json')
    quegong_all= readjson(data_root+'quegong_bottomCard.json')
    fugong_daily_date=set([d['date'] for d in fugong_daily])
    quegong_daily_date=set([d['date'] for d in quegong_daily])
    fugong_all_date=set(fugong_all['dateList'])
    quegong_all_date=set(quegong_all['dateList'])
    print(fugong_all_date.difference(quegong_all_date))
    print(quegong_all_date.difference(fugong_all_date))
    print(fugong_daily_date.difference(quegong_daily_date))
    print(quegong_daily_date.difference(fugong_daily_date))
    print(fugong_all_date.difference(fugong_daily_date))
    print(fugong_daily_date.difference(fugong_all_date))

def histroy_fugong_quegong_table():
    with open("./stat/shortName.json","r",encoding="utf-8") as jsonFile:
        cities_ = json.loads(jsonFile.read())
    
    fugong = readjson(data_root+'fugong_daily.json')
    quegong = readjson(data_root+'quegong_daily.json')['data']
    cities=fugong['city']
    fugong=fugong['data']
    all_date=[d['date'] for d in fugong]

    tmp=readjson('stat/cities_codes.json')
    city2code=tmp['city2code']
    code2province=tmp['code2province']
    
    city2gdp={}
    with open('stat/全国GDP.csv','r',encoding='utf-8') as f:
        f_csv=csv.reader(f)
        for ind,row in enumerate(f_csv):
            if(ind==0):
                continue
            cname=cleantxt(row[0],cities_)
            city2gdp[cname]=float(row[1])
    
    province2gdp={}
    for ind,c in enumerate(cities):
        if(c in provinces):
            continue
        c=get_shortname(c,cities_)
        gdp=city2gdp[c]
        code=city2code[c][0:2]
        sf=get_shortname(code2province[code],cities_)
        province2gdp[sf]=province2gdp.get(sf,0)+gdp

    wt=MyWriter(feed_root+'各省复工复产历史数据.csv',['日期','复工指数','缺工指数','省份'],index='序号')
    def all_up(wt,all_date):
        fugong = readjson(data_root+'fugong_bottomCard.json')
        quegong= readjson(data_root+'quegong_bottomCard.json')
        for ind,d in enumerate(all_date):
            f=clip(fugong['value'][ind])
            q=clip(quegong['value'][ind])
            r=(f+(1-q))/2
            wt.insert([format_date(d),f,q,'全国'])
    all_up(wt,all_date)
    date2sf2qg={}
    date2sf2fg={}
    for f_item,q_item in zip(fugong,quegong):
        date=f_item['date']
        sf2quegong={}
        sf2fugong={}
        for ind,c in enumerate(cities):
            c=get_shortname(c,cities_)
            gdp=city2gdp[c]
            code=city2code[c][0:2]
            sf=get_shortname(code2province[code],cities_)
            sgdp=province2gdp[sf]
            f=clip(f_item['value'][ind])
            q=clip(q_item['value'][ind])
            sf2fugong[sf]=sf2fugong.get(sf,0)+f*gdp/sgdp
            sf2quegong[sf]=sf2quegong.get(sf,0)+q*gdp/sgdp
        date2sf2fg[date]=sf2fugong
        date2sf2qg[date]=sf2quegong
    for sf,gdp in province2gdp.items():
        for date in all_date:
            f=date2sf2fg[date][sf]
            q=date2sf2qg[date][sf]
            wt.insert([format_date(date),f,q,sf])
    wt.save()


def china_map(indextype):
    # shortName里面的地名不包含“省”“市”
    with open("./stat/shortName.json","r",encoding="utf-8") as jsonFile:
        cities = json.loads(jsonFile.read())
    # 由百度数据计算出来的缺工复工指数
    with open(data_root+indextype+"_daily.json","r",encoding="utf-8") as jsonFile:
        fugong = json.loads(jsonFile.read())
    content = []
    dateList = []
    fugong_city=[get_shortname(c,cities) for c in fugong['city']]
    for item in fugong["data"]:
        # 日期只要月-日
        dateList.append(item["date"][-5:])
        content.append([clip(v) for v in item['value']])
    df = pd.DataFrame(content, columns=fugong_city)
    with open(data_root+"china-cities-new.json","r",encoding="utf-8") as jsonFile:
        data = json.loads(jsonFile.read())
    for i in range(len(data["features"])):
        name_org = data["features"][i]["properties"]["name"]
        name = get_shortname(name_org,cities)
        if name in fugong_city:
            fugongvalue = df[name].tolist()
            fugongList = {}
            for j in range(len(dateList)):
                fugongList[dateList[j]] = fugongvalue[j]
            # 把要绑定的数据放在temp里，再放进properties
            temp = {
                "name": name,
                indextype: df[name].tolist()[-1],
                indextype+"List": fugongList
            }
            data["features"][i]["properties"] = temp
        elif name == "台湾":
            temp = {
                "name": name,
                indextype: 0.05,
            }
            data["features"][i]["properties"] = temp
        else:
            temp = {
                "name": name,
                indextype: 0.05,
            }
            data["features"][i]["properties"] = temp
    with open(feed_root+"china-cities-"+indextype+".json","w",encoding="utf-8") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)

if __name__=='__main__':
    # today=strftime(r"%Y%m%d",localtime(time()))

    today=20200321
    print(today)
    bottomCard_quegong(today)
    bottomCard_fugong(today)
    calFugong(start=20200210, end=today)
    calQuegong(start=20200210,end=today)
    sideCard(today)
    assert_date()

    left_table()
    right_bars()
    histroy_fugong_quegong_table()
    china_map('fugong')
    china_map('quegong')