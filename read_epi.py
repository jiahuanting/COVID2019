import xlrd
import xlwt
import pickle as pk
import re
import datetime
import time
import json
import csv
import os
from namemap import nameMap
import pandas as pd

def readjson(file):
    with open(file,'r',encoding='utf-8')as f:
        data=json.load(f)
    return data

feed_root='feed/'
data_root='stat/data/'
name_trans={'Singapore Rep.':'Singapore',
        # "United States":"United States of America",
        "United States":'USA',
        'United Kingdom':"UK",
        "Korea":"South Korea"}
world_pop=readjson(data_root+'worldPopulation.json')
ch2en=readjson('stat/'+'ch2en.json')

def write_to_pk(data,file):
    with open(file,'wb') as f:
        pk.dump(data,f)

def read_from_pk(file):
    with open(file,'rb') as f:
        data=pk.load(f)
    return data

def writejson(file,data):
    with open(file,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False)

def format_date(date):
    date=date.split('/')
    year=date[0]
    month=date[1].lstrip('0')
    day=date[2].lstrip('0')
    return f'{month} / {day}'

class MyWriter():
    def __init__(self,path,header,index=None,lift=None,force_int=[]):
        self.data=[]
        self.index=index
        self.header=header
        self.path=path
        if(index is not None):
            self.header.append(index)
        self.lift=lift
        self.force_int=force_int
    def insert(self,dt):
        l=[]
        for ind,d in enumerate(dt):
            if isinstance(d,float) and ind in self.force_int:
                l.append(int(d))
            elif isinstance(d,float):
                l.append(round(d,3))
            else:
                l.append(d)
        self.data.append(l)
    def save(self):
        with open(self.path,'w',newline='',encoding='gbk') as f:
            writer=csv.writer(f)
            writer.writerow(self.header)
            remain=[]
            cnt=0
            if self.lift is not None:
                liftind,liftfliter=self.lift
                for d in self.data:
                    if d[liftind]==liftfliter:
                        cnt=cnt+1
                        if self.index is not None:
                            writer.writerow(d+[cnt])
                        else:
                            writer.writerow(d)
                    else:
                        remain.append(d)
            else:
                remain=self.data
            for d in remain:
                cnt=cnt+1
                if self.index is not None:
                    writer.writerow(d+[cnt])
                else:
                    writer.writerow(d)

class XLSReader():
    def __init__(self,name,sheet_ind):
        print('read:'+name)
        data=xlrd.open_workbook(name)
        self.table=data.sheet_by_index(sheet_ind)
        self.nrows=self.table.nrows
        self.ncols=self.table.ncols
        self.header=[]
        for col in range(self.ncols):
            h=self.cell_value(self.table.cell(0,col))
            self.header.append(h)
        # print(f"header is :{self.header}")

    def cell_value(self,cell):
        ctp=cell.ctype
        if ctp == 0:#empty
            return 0
        elif ctp == 3:
            tup=xlrd.xldate_as_tuple(cell.value,0)
            return '%04d/%02d/%02d'%(tup[0],tup[1],tup[2])
        elif ctp == 5:
            print('type error')
            raise Exception 
        else:
            return cell.value

    def __len__(self):
        return self.nrows

    def __getitem__(self,index):
        if index >= self.__len__():
            raise IndexError
        ret={}
        for col in range(self.ncols):
            item = self.table.cell(index+1,col)
            item=self.cell_value(item)
            ret[self.header[col]]=item
        return ret

def date_add(datestr,offset):
    day=datetime.datetime.strptime(datestr, "%Y/%m/%d")
    last=day+datetime.timedelta(days=offset)
    last=datetime.datetime.strftime(last,"%Y/%m/%d")
    return last

class EPI_Reader():
    countries=['全球_不含中国','全国','韩国', '泰国', '新加坡', '日本', '伊朗', '美国', \
    '意大利', '法国', '德国', '西班牙', '荷兰', '瑞典', '比利时', '英国', \
    '瑞士', '希腊', '加拿大', '马来西亚', '菲律宾', '澳大利亚', '丹麦', '挪威', \
    '奥地利', '卢森堡', '卡塔尔', '爱尔兰', '葡萄牙', '以色列', '芬兰', '捷克', \
    '巴西', '智利', '巴基斯坦','俄罗斯','爱沙尼亚','斯洛文尼亚']   
    def __init__(self):
        epi_path='stat/epi_initial.xlsx'
        csv_path='results/'
        confirmed=XLSReader(epi_path,0)
        recover=XLSReader(epi_path,1)
        death=XLSReader(epi_path,2)
        dates=confirmed.header[3:]
        self.current_date=dates[-1]
        self.dates=dates
        self.recover=recover
        self.confirmed=confirmed
        self.death=death
        self.csv_path=csv_path
        self.epi_path=epi_path
        self.ch2en=readjson('stat/ch2en.json')
    
    def get_rate(self):
        epi_path='stat/epi_initial.xlsx'
        csv_path='results/'
        confirmed=XLSReader(epi_path,0)
        recover=XLSReader(epi_path,1)
        death=XLSReader(epi_path,2)
        rate={}
        rate_default={}
        for cofrow,recrow,dthrow in zip(confirmed,recover,death):
            country=cofrow['city']
            if country not in self.countries:
                continue
            tmp={}
            for date in self.dates:
                rec=recrow[date]
                dth=dthrow[date]
                cof=cofrow[date]-rec-dth
                tmp[date] = 0 if (rec+dth)==0 else dth/(rec+dth)  
            rate_default[country]=tmp[self.dates[-1]]
            rate[country]=tmp          
        self.rateByCountry=rate
        self.rate_default=rate_default
            
    def get_csv(self,country):
        def get_once(csvData,colname,cur):
            try:
                return csvData.loc[csvData['Date']==cur,colname].tolist()[0]
            except Exception as e:
                # print(e)
                return None
        def get_china(csvData,colname,cur):
            csvData_wh,csvData_hb,csvData_qg=csvData
            try:
                wh=csvData_wh.loc[csvData_wh['Date']==cur,colname].tolist()[0]
                hb=csvData_hb.loc[csvData_hb['Date']==cur,colname].tolist()[0]
                qg=csvData_qg.loc[csvData_qg['Date']==cur,colname].tolist()[0]
                return wh+hb+qg
            except Exception as e:
                # print(e)
                return None

        filename=country + '.csv'
        file_list=os.listdir(self.csv_path)
        if filename not in file_list:
            print('not such file: '+filename)
            return False
        if '全国' in filename:
            csvData_wh=pd.read_csv(self.csv_path + '武汉市.csv')[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm','Remove','Predict_cure'] ]
            csvData_hb=pd.read_csv(self.csv_path + '湖北_不含武汉.csv')[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm','Remove','Predict_cure'] ]
            csvData_qg=pd.read_csv(self.csv_path + '全国_不含湖北.csv')[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm','Remove','Predict_cure'] ]
            csvData=(csvData_wh,csvData_hb,csvData_qg)
        else:
            csvData = pd.read_csv(self.csv_path + filename)[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm','Remove'] ]
        day = datetime.datetime.strptime(self.current_date, "%Y/%m/%d")
        predict=[]
        remain=[]
        pred_daily_new=[]
        death=[]
        cure=[]
        dateList=[]
        for d in range(-14,31):
            cur = day+datetime.timedelta(days=d)
            cur = datetime.datetime.strftime(cur,"%Y/%m/%d")
            dateList.append(cur)
            if '全国' in filename:
                predict.append(get_china(csvData,'Predict_confirm',cur))
                remain.append(get_china(csvData,'Remain_confirm',cur))
                pred_daily_new.append(get_china(csvData,'Dailynew_confirm',cur))
                rmv=get_china(csvData,'Remove',cur)
                dth=rmv*self.rateByCountry[country].get(cur,self.rate_default[country])
                c=rmv-dth
                death.append(dth)
                cure.append(c)
            else:
                predict.append(get_once(csvData,'Predict_confirm',cur))
                remain.append(get_once(csvData,'Remain_confirm',cur))
                pred_daily_new.append(get_once(csvData,'Dailynew_confirm',cur))
                rmv=get_once(csvData,'Remove',cur)
                if(rmv is not None):
                    dth=rmv*self.rateByCountry[country].get(cur,self.rate_default[country])
                    c=rmv-dth
                    death.append(dth)
                    cure.append(c)
                else:
                    death.append(None)
                    cure.append(None)        

        self.predict=predict
        self.remain=remain
        self.pred_daily_new=pred_daily_new
        self.pred_death=death
        self.pred_cure=cure
        self.dateList=dateList

        props={'name':country}
        if "全国" in filename:
            all_dates=csvData_hb['Date'].tolist()
            func=get_china
            props['scale']=int(func(csvData,'Predict_confirm','2020/06/14'))
        else:
            all_dates=csvData['Date'].tolist()
            func=get_once
            props['scale']=int(func(csvData,'Predict_confirm',all_dates[-1]))

        f_inc=func(csvData,'Predict_confirm',date_add(self.current_date,14))-\
              func(csvData,'Predict_confirm',self.current_date)
        props['f_inc']=int(f_inc)
        m,mdate=0,None
        for d in all_dates:
            cur_add=func(csvData,'Dailynew_confirm',d)
            if cur_add is not None and m < cur_add:
                m=cur_add
                mdate=d  
        props['max_inc_date']=mdate
        self.props=props      
        return True

    def country_level(self,wt1,wt2,wt3,country,cofrow,recrow,dthrow):
        country=self.ch2en[country]
        country=name_trans.get(country,country)
        flg=False
        for date,p,r,n,dth,rec in zip(self.dateList,self.predict,self.remain,self.pred_daily_new,self.pred_death,self.pred_cure):
            if flg:
                wt1.insert([
                    format_date(date),
                    p,r,n,dth,rec,
                    None,None,None,None,None,
                    country
                ])
                continue
            else:
                a_conf=cofrow[date]
                a_rec=recrow[date]
                a_dth=dthrow[date]
                a_rem=a_conf-a_rec-a_dth
                last=cofrow[date_add(date,-1)]
                a_new=a_conf-last
                wt1.insert([
                    format_date(date),
                    p,r,n,dth,rec,
                    a_conf,a_rem,a_new,a_dth,a_rec,
                    country
                ])
            if date==self.current_date:
                flg=True

        today_ind=self.dateList.index(self.current_date)
        inc=self.predict[today_ind+14]-self.predict[today_ind]
        pop=float(world_pop[country])
        rat=inc/pop*1000000
        wt2.insert([int(inc),rat,country])

        props=self.props
        props['a_inc']=int(cofrow[self.current_date]-cofrow[date_add(self.current_date,-14)])
        props['a_rate']=props['a_inc']/pop*1000000
        props['f_rate']=props['f_inc']/pop*1000000
        props['current']=int(cofrow[self.current_date])
        props['name']=country
        self.map_data.append(props)

        wt3.insert([int(cofrow[self.current_date]),country])

        print(country,'ok')

    def main(self):
        self.map_data=[]
        confirmed=self.confirmed
        recover=self.recover
        death=self.death
        wt1=MyWriter(feed_root+'全球疫情预测.csv',['日期','预测确诊','预测在治','预测新增','预测死亡'\
        ,'预测治愈','实际确诊','实际在治','实际新增','实际死亡','实际治愈','国家'],\
        index='编号',lift=[11,'Global (except China)'],
        force_int=[1,2,3,4,5,6,7,8,9,10])
        wt2=MyWriter(feed_root+'未来预测数据.csv',['未来14天确诊数目','未来14天感染率','国家'],\
        force_int=[0])
        wt3=MyWriter(feed_root+'全球疫情现状.csv',['患病人数','国家'],\
        lift=[1,'Global (except China)'],\
        force_int=[0])
        for cofrow,recrow,dthrow in zip(confirmed,recover,death):
            country=cofrow['city']
            if country not in self.countries:
                print('no such country',country)
                continue
            if not self.get_csv(country):
                continue
            if country=='全国':
                country='中国'
            self.country_level(wt1,wt2,wt3,country,cofrow,recrow,dthrow)
        wt1.save()
        wt2.save()
        wt3.save()
        writejson(feed_root+'world_map_data_short.json',self.map_data)
        print('current date is',self.current_date)

def dump_geo_json():
    map_data=readjson(feed_root+'world_map_data_short.json')
    country_geojson=readjson(data_root+'country_geojson.json')['features']
    geo_data={}
    for item in country_geojson:
        geo_data[item['properties']['name']]=item
    features=[]
    for props in map_data:
        name=props['name']
        if name in ['Global (except China)']:
            continue
        node=geo_data[name]
        node['properties']=props
        features.append(node)
    geojson={"type":"FeatureCollection","features":features}
    writejson(feed_root+"world_pred.json",geojson)


import matplotlib.pyplot as plt

def plot_curve(countrylist,curdate):
    epi_path='stat/epi_initial.xlsx'
    csv_path='results/'
    confirmed=XLSReader(epi_path,0)
    recover=XLSReader(epi_path,1)
    death=XLSReader(epi_path,2)
    rate={}
    rate_default={}
    day = datetime.datetime.strptime(curdate, "%Y/%m/%d")
    for cofrow,recrow,dthrow in zip(confirmed,recover,death):
        country=cofrow['city']
        if country not in countrylist:
            continue
        predict=[]
        actual=[]
        csvData = pd.read_csv('results/'+country+'.csv')[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm','Remove'] ]
        p_date=[]
        a_date=[]
        for d in range(-14,1):
            cur = day+datetime.timedelta(days=d)
            cur = datetime.datetime.strftime(cur,"%Y/%m/%d")
            actual.append(cofrow[cur])
            a_date.append(cur)
        
        for d in range(-5,31):
            cur = day+datetime.timedelta(days=d)
            cur = datetime.datetime.strftime(cur,"%Y/%m/%d")
            predict.append(csvData.loc[csvData['Date']==cur,"Predict_confirm"].tolist()[0])
            p_date.append(cur)
        plt.plot(a_date,actual)
        plt.plot(p_date,predict)
        plt.title(ch2en[country])
        plt.show()
        
                  

if __name__=='__main__':
    epi=EPI_Reader()
    epi.get_rate()
    epi.main()
    dump_geo_json()
    # plot_curve(['韩国'],'2020/3/25')