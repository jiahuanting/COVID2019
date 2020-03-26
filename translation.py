#!/usr/bin/python
# -*- coding: UTF-8 -*-
translation={
    '省份':'Province',
    '复工指数':"Resumption",
    "缺工指数":"Absence",
    "恢复指数":"",
    '日期':'Date',
    '全国':'China',
    '迁出指数':'Increasing of people',
    '迁入指数':'Decreasing of people',
    '城市':'City',
    '编号':'Index',
    '序号':'Index',

}
province2gdp={"河北省": 36010.3, "山西省": 16818.1, "辽宁省": 25315.4, "吉林": 15074.6, "黑龙江省": 16361.6, "江苏省": 92595.4, "浙江省": 56197.2, "安徽省": 30006.8, "福建省": 35804.0, "江西省": 21984.8, "山东省": 76469.7, "河南省": 48055.9, "湖北省": 39366.6, "湖南省": 36425.8, "广东省": 97277.8, "海南": 4832.1, "四川省": 40678.1, "贵州省": 14806.5, "云南省": 17881.1, "陕西省": 24438.3, "甘肃省": 8246.1, "青海省": 2865.2, "内蒙古自治区": 17289.2, "广西壮族自治区": 20352.5, "西藏自治区": 1477.6, "宁夏回族自治区": 3705.2, "新疆维吾尔自治区": 12199.1, "北京": 30320.0, "上海": 32679.9, "天津": 18809.6, "重庆": 20363.2}
city2gdp={"铁门关": 18.06, "神农架": 25.51, "五指山": 28.99, "果洛": 41.45, "北屯": 43.91, "白沙": 47.14, "阿里": 47.24, "保亭": 48.63, "琼中": 49.5, "玉树": 53.61, "屯昌县": 70.19, "图木舒克": 82.92, "海北": 83.53, "黄南": 88.33, "定安县": 90.28, "那曲": 119.82, "大兴安岭": 122.8, "昌江": 125.41, "乐东": 126.97, "克孜勒苏": 128.89, "林芝": 133.33, "陵水": 151.01, "甘南": 155.73, "海南": 4832.1, "怒江": 161.56, "五家渠": 162.41, "山南": 164.32, "昌都": 169.83, "临高县": 176.23, "东方": 177.91, "日喀则": 187.75, "万宁": 203.9, "文昌": 205.98, "迪庆": 217.52, "七台河": 250.32, "临夏": 255.35, "琼海": 264.1, "金昌": 264.24, "伊春": 274.15, "鹤岗": 282.9, "阿勒泰": 284.09, "澄迈县": 288.74, "甘孜": 291.2, "阿拉尔": 299.34, "嘉峪关": 299.62, "固原": 303.19, "黄冈": 305.19, "和田": 305.57, "阿坝": 306.67, "吐鲁番": 310.59, "儋州": 322.97, "铜川": 327.96, "博尔塔拉": 330.34, "石河子": 333.86, "阿拉善盟": 342.32, "丽江": 350.76, "定西": 356.26, "陇南": 379.23, "德宏": 381.06, "平凉": 395.17, "中卫": 402.99, "哈密": 403.68, "张掖": 407.71, "西双版纳": 417.79, "兴安盟": 417.92, "阜新": 446.0, "海东": 451.5, "武威": 469.27, "锡林郭勒盟": 472.48, "黑河": 505.1, "双鸭山": 507.0, "白银": 511.6, "天门": 528.25, "吴忠": 534.5, "鸡西": 535.2, "拉萨": 540.78, "乌海": 572.23, "张家界": 578.92, "三亚": 595.51, "酒泉": 596.9, "济源": 600.12, "贺州": 602.63, "湘西": 605.05, "石嘴山": 605.92, "铁岭": 616.6, "白城": 618.28, "塔城": 620.25, "普洱": 624.59, "海西": 625.27, "临沧": 630.02, "巴中": 645.88, "雅安": 646.1, "天水": 652.05, "白山": 660.06, "来宾": 663.69, "辽源": 668.65, "潜江": 671.86, "黄山": 677.9, "池州": 684.9, "延边": 706.33, "庆阳": 708.15, "仙桃": 718.66, "阳泉": 733.7, "保山": 738.1, "防城港": 741.62, "河池": 788.3, "广元": 801.85, "葫芦岛": 812.8, "巴彦淖尔": 813.1, "丹东": 816.7, "鹰潭": 818.98, "本溪": 823.1, "商洛": 824.77, "朝阳": 831.4, "通化": 836.13, "景德镇": 846.6, "云浮": 849.13, "安顺": 849.4, "文山": 859.06, "鹤壁": 861.9, "辽阳": 869.7, "恩施": 870.95, "昭通": 889.54, "喀什": 890.12, "克拉玛依": 898.1, "崇左": 907.62, "汕尾": 920.32, "乌兰察布": 938.87, "四平": 939.83, "淮北": 985.2, "忻州": 989.1, "鄂州": 1005.3, "河源": 1006.0, "萍乡": 1009.05, "随州": 1011.19, "佳木斯": 1012.0, "楚雄": 1024.33, "新余": 1027.34, "阿克苏": 1027.4, "巴音郭楞": 1027.5, "黔东南": 1036.62, "抚顺": 1048.8, "朔州": 1065.6, "资阳": 1066.5, "铜仁": 1066.52, "潮州": 1067.28, "梅州": 1110.21, "大理": 1122.44, "淮南": 1133.3, "安康": 1133.77, "黔西南": 1163.77, "贵港": 1169.88, "攀枝花": 1173.52, "锦州": 1192.4, "盘锦": 1216.6, "遂宁": 1221.39, "铜陵": 1222.4, "北海": 1229.84, "漯河": 1236.7, "广安": 1250.2, "呼伦贝尔": 1252.9, "眉山": 1256.02, "大同": 1271.8, "亳州": 1277.2, "西宁": 1286.41, "六安": 1288.1, "通辽": 1301.6, "钦州": 1309.82, "黔南": 1313.46, "舟山": 1316.7, "宣城": 1317.2, "齐齐哈尔": 1333.84, "梧州": 1338.1, "韶关": 1343.91, "牡丹江": 1344.7, "营口": 1346.7, "阳江": 1350.31, "晋城": 1351.9, "绥化": 1359.6, "百色": 1361.76, "咸宁": 1362.42, "昌吉": 1367.3, "松原": 1372.51, "抚州": 1382.4, "丽水": 1394.67, "自贡": 1406.71, "赤峰": 1406.8, "内江": 1411.75, "吕梁": 1420.3, "临汾": 1440.0, "晋中": 1447.6, "衢州": 1470.58, "汉中": 1471.88, "西藏自治区": 1477.6, "红河": 1478.57, "承德": 1481.5, "玉溪": 1493.0, "运城": 1509.6, "海口": 1510.51, "怀化": 1513.27, "六盘水": 1525.69, "三门峡": 1528.12, "凉山": 1533.19, "张家口": 1536.6, "娄底": 1540.41, "衡水": 1558.7, "延安": 1558.91, "清远": 1565.19, "黄石": 1587.33, "乐山": 1615.09, "宿州": 1630.22, "秦皇岛": 1635.56, "长治": 1645.6, "濮阳": 1654.47, "达州": 1690.17, "泸州": 1694.97, "玉林": 1699.54, "蚌埠": 1714.66, "吉安": 1742.23, "十堰": 1747.8, "鞍山": 1751.1, "益阳": 1758.38, "阜阳": 1759.5, "渭南": 1767.71, "邵阳": 1782.65, "南平": 1792.51, "滁州": 1801.7, "永州": 1805.65, "荆门": 1847.89, "银川": 1901.48, "孝感": 1912.9, "伊犁": 1917.21, "安庆": 1917.6, "马鞍山": 1918.1, "毕节": 1921.43, "宁德": 1942.8, "开封": 2002.23, "南充": 2006.03, "曲靖": 2013.36, "宜宾": 2026.37, "桂林": 2045.18, "荆州": 2082.18, "平顶山": 2135.2, "邢台": 2150.76, "揭阳": 2152.47, "湘潭": 2161.4, "宜春": 2180.85, "肇庆": 2201.8, "日照": 2202.17, "吉林": 2208.85, "上饶": 2212.8, "德阳": 2213.9, "莆田": 2242.41, "宝鸡": 2265.16, "绵阳": 2303.82, "三明": 2353.72, "驻马店": 2370.32, "焦作": 2371.5, "咸阳": 2376.45, "信阳": 2387.8, "商丘": 2389.03, "郴州": 2391.9, "安阳": 2393.2, "龙岩": 2393.3, "枣庄": 2402.38, "汕头": 2512.05, "新乡": 2526.55, "株洲": 2631.5, "滨州": 2640.52, "周口": 2687.22, "九江": 2700.19, "湖州": 2719.07, "兰州": 2732.94, "宿迁": 2750.72, "连云港": 2771.7, "大庆": 2801.2, "赣州": 2807.24, "许昌": 2830.6, "青海省": 2865.2, "江门": 2900.41, "呼和浩特": 2903.5, "珠海": 2914.74, "遵义": 3000.23, "湛江": 3008.39, "衡阳": 3046.03, "柳州": 3053.65, "乌鲁木齐": 3060.14, "保定": 3070.9, "菏泽": 3078.78, "茂名": 3092.18, "廊坊": 3108.2, "聊城": 3152.15, "芜湖": 3278.53, "德州": 3380.3, "常德": 3394.2, "岳阳": 3411.01, "邯郸": 3454.6, "南阳": 3566.77, "淮安": 3601.25, "中山": 3632.7, "威海": 3641.48, "泰安": 3651.5, "沧州": 3676.4, "宁夏回族自治区": 3705.2, "鄂尔多斯": 3763.2, "贵阳": 3798.45, "东营": 3801.78, "榆林": 3848.62, "包头": 3867.63, "太原": 3884.48, "漳州": 3947.63, "镇江": 4050.0, "宜昌": 4064.18, "金华": 4100.23, "惠州": 4103.05, "南宁": 4118.83, "襄阳": 4309.8, "洛阳": 4640.8, "济宁": 4650.57, "临沂": 4717.8, "厦门": 4791.41, "嘉兴": 4871.98, "台州": 4874.67, "淄博": 5068.4, "泰州": 5107.63, "昆明": 5206.9, "南昌": 5274.67, "绍兴": 5416.9, "扬州": 5466.17, "盐城": 5487.08, "温州": 6006.16, "石家庄": 6082.6, "潍坊": 6156.8, "沈阳": 6292.4, "哈尔滨": 6300.5, "唐山": 6530.15, "徐州": 6755.23, "常州": 7050.27, "长春": 7175.7, "大连": 7668.48, "合肥": 7822.9, "烟台": 7832.58, "济南": 7856.6, "福州": 7856.81, "甘肃省": 8246.1, "东莞": 8278.59, "西安": 8349.86, "南通": 8427.0, "泉州": 8467.98, "佛山": 9935.88, "郑州": 10143.32, "宁波": 10745.5, "长沙": 11003.41, "无锡": 11438.62, "青岛": 12001.5, "新疆维吾尔自治区": 12199.1, "南京": 12820.4, "杭州": 13509.15, "贵州省": 14806.5, "武汉": 14847.29, "成都": 15342.77, "黑龙江省": 16361.6, "山西省": 16818.1, "内蒙古自治区": 17289.2, "云南省": 17881.1, "苏州": 18597.47, "天津": 18809.6, "广西壮族自治区": 20352.5, "重庆": 20363.2, "江西省": 21984.8, "广州": 22859.35, "深圳": 24221.98, "陕西省": 24438.3, "辽宁省": 25315.4, "安徽省": 30006.8, "北京": 30320.0, "上海": 32679.9, "福建省": 35804.0, "河北省": 36010.3, "湖南省": 36425.8, "湖北省": 39366.6, "四川省": 40678.1, "河南省": 48055.9, "浙江省": 56197.2, "山东省": 76469.7, "江苏省": 92595.4, "广东省": 97277.8, "三沙市": 0.0, "双河": 0.0, "可克达拉市": 0.0, "昆玉市": 0.0}

import requests
import json
def readjson(file):
    with open(file,'r',encoding='utf-8')as f:
        data=json.load(f)
    return data

def writejson(file,data):
    with open(file,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False)

def translate(chinese):
    url='http://fanyi.youdao.com/translate'
    r=requests.get(url+'?doctype=json&type=ZH_CN2EN&i='+chinese).json()
    return r['translateResult'][0][0]['tgt']

if __name__=='__main__':
    trans=translation
    for p in province2gdp:
        trans[p]=translate(p)
        print(p,trans[p])
    for p in city2gdp:
        trans[p]=translate(p)
        print(p,trans[p])
    writejson('stat/translation.json',trans)