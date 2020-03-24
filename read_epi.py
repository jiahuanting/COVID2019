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

def write_to_pk(data,file):
    with open(file,'wb') as f:
        pk.dump(data,f)

def read_from_pk(file):
    with open(file,'rb') as f:
        data=pk.load(f)
    return data

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

feed_root='feed/'
data_root='stat/data/'

class EPI_Reader():
    countries=['全国','韩国', '泰国', '新加坡', '日本', '伊朗', '美国', \
    '意大利', '法国', '德国', '西班牙', '荷兰', '瑞典', '比利时', '英国', \
    '瑞士', '希腊', '加拿大', '马来西亚', '菲律宾', '澳大利亚', '丹麦', '挪威', \
    '奥地利', '卢森堡', '卡塔尔', '爱尔兰', '葡萄牙', '以色列', '芬兰', '捷克', \
    '巴西', '智利', '巴基斯坦']   
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
    
    def get_rate(self):
        epi_path='stat/epi_initial.xlsx'
        csv_path='results/'
        confirmed=XLSReader(epi_path,0)
        recover=XLSReader(epi_path,1)
        death=XLSReader(epi_path,2)
        rate={}
        for cofrow,recrow,dthrow in zip(confirmed,recover,death):
            city=cofrow['city']
            if city not in self.countries:
                continue
            date=self.dates[-1]
            rec=recrow[date]
            dth=dthrow[date]
            cof=cofrow[date]-rec-dth
            rate[city] = 0 if (rec+dth)==0 else dth/(rec+dth)
        self.rateByCountry=rate
            
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
            csvData_wh=pd.read_csv(self.csv_path + '武汉市.csv')[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm','Dailynew_remove','Dailynew_cure'] ]
            csvData_hb=pd.read_csv(self.csv_path + '湖北_不含武汉.csv')[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm','Dailynew_remove','Dailynew_cure'] ]
            csvData_qg=pd.read_csv(self.csv_path + '全国_不含湖北.csv')[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm','Dailynew_remove','Dailynew_cure'] ]
            csvData=(csvData_wh,csvData_hb,csvData_qg)
        else:
            csvData = pd.read_csv(self.csv_path + filename)[ ["Date","Predict_confirm","Remain_confirm",'Dailynew_confirm','Dailynew_remove'] ]
        day = datetime.datetime.strptime(self.current_date, "%Y/%m/%d")
        predict=[]
        remain=[]
        pred_daily_new=[]
        death=[]
        cure=[]
        dateList=[]
        for d in range(-13,31):
            cur = day+datetime.timedelta(days=d)
            cur = datetime.datetime.strftime(cur,"%Y/%m/%d")
            dateList.append(cur)
            if '全国' in filename:
                predict.append(get_china(csvData,'Predict_confirm',cur))
                remain.append(get_china(csvData,'Remain_confirm',cur))
                pred_daily_new.append(get_china(csvData,'Dailynew_confirm',cur))
                c= get_china(csvData,'Dailynew_cure',cur)
                rmv=get_china(csvData,'Dailynew_remove',cur)
                dth=rmv-c
                death.append(dth)
                cure.append(c)
            else:
                predict.append(get_once(csvData,'Predict_confirm',cur))
                remain.append(get_once(csvData,'Remain_confirm',cur))
                pred_daily_new.append(get_once(csvData,'Dailynew_confirm',cur))
                rmv=get_once(csvData,'Dailynew_remove',cur)
                if(rmv is not None):
                    dth=rmv*self.rateByCountry[country]
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
            all_dates=csvData_hb['Date'].to_list()
            func=get_china
            props['scale']=func(csvData,'Predict_confirm','2020/06/14')
        else:
            all_dates=csvData['Date'].to_list()
            func=get_once
            props['scale']=func(csvData,'Predict_confirm',all_dates[-1])

        f_inc=func(csvData,'Predict_confirm',date_add(self.current_date,14))-\
              func(csvData,'Predict_confirm',self.current_date)
        props['f_inc']=f_inc
        m,mdate=0,None
        for d in all_dates:
            cur_add=func(csvData,'Dailynew_confirm',d)
            if cur_add is not None and m < cur_add:
                m=cur_add
                mdate=d  
        props['max_inc_date']=mdate
        self.props=props      
        return True

    def main(self):
        name_trans={'Singapore Rep.':'Singapore',
        "United States":"United States of America",
        "Korea":"South Korea"}
        map_data=[]
        ch2en=readjson('stat/ch2en.json')
        world_pop=readjson(data_root+'worldPopulation.json')
        confirmed=self.confirmed
        recover=self.recover
        death=self.death
        wt1=MyWriter(feed_root+'全球疫情预测.csv',['日期','预测确诊','预测在治','预测新增','预测死亡'\
        ,'预测治愈','实际确诊','实际在治','实际新增','实际死亡','实际治愈','国家'],index='编号')
        wt2=MyWriter(feed_root+'未来预测数据.csv',['未来14天确诊数目','未来14天感染率','国家'])
        for cofrow,recrow,dthrow in zip(confirmed,recover,death):
            city=cofrow['city']
            if city not in self.countries:
                continue
            if not self.get_csv(city):
                continue
            if city=='全国':
                city='中国'
            city=ch2en[city]
            flg=False
            for date,p,r,n,dth,rec in zip(self.dateList,self.predict,self.remain,self.pred_daily_new,self.pred_death,self.pred_cure):
                if flg:
                    wt1.insert([
                        date,
                        p,r,n,dth,rec,
                        None,None,None,None,None,
                        city
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
                        date,
                        p,r,n,dth,rec,
                        a_conf,a_rem,a_new,a_dth,a_rec,
                        city
                    ])
                if date==self.current_date:
                    flg=True

            today_ind=self.dateList.index(self.current_date)
            inc=self.predict[today_ind+14]-self.predict[today_ind]
            city=name_trans.get(city,city)
            pop=float(world_pop[city])
            rat=inc/pop*1000000
            wt2.insert([inc,rat,city])
            props=self.props
            props['a_inc']=cofrow[self.current_date]-cofrow[date_add(self.current_date,-14)]
            props['a_rate']=props['a_inc']/pop*1000000
            props['f_rate']=props['f_inc']/pop*1000000
            props['current']=cofrow[self.current_date]
            props['name']=city
            map_data.append(props)
            print(city,'ok')
        wt1.save()
        wt2.save()
        writejson(feed_root+'world_map_data_short.json',map_data)
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
        node=geo_data[name]
        node['properties']=props
        features.append(node)
    geojson={"type":"FeatureCollection","features":features}
    writejson(feed_root+"world_pred.json",geojson)

if __name__=='__main__':
    epi=EPI_Reader()
    epi.get_rate()
    epi.main()
    dump_geo_json()