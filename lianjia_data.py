from pyecharts import *
import pandas as pd
from pandas import *
from matplotlib import pyplot as plt
data = pd.read_csv('C:/Users/hanhui/Desktop/lianjia.csv')
regions = ['朝阳','海淀','丰台','石景山','通州','昌平','亦庄开发区','顺义','房山','门头沟']
#数量柱状图
room_count = []
for i in regions:
    num = len(data[data['行政区'] == i])
    room_count.append(num)

room_bar = Bar('北京租房图表',width=1000,title_text_size=20)
room_bar.add('数量',regions,room_count)
room_bar.render()


#租金柱状图
money_means = []
for i in regions:
    money_data = data[data['行政区'] == i]
    money_means.append(money_data['房屋租金'].mean())

money_bar = Bar("各地区平均租金对比", title_pos='left', width=1000,title_text_size=20)
money_bar.add('平均租金',regions,money_means)
money_bar.render()

#面积柱状图
size_means = []
for i in regions:
    size_data = data[data['行政区'] == i]
    size_means.append(size_data['房屋大小'].mean())
size_bar = Bar("各地区平均房屋大小对比", title_pos='left', width=1000, title_text_size=20)
size_bar.add('平均大小',regions,size_means)
size_bar.render()

#租金饼图
rent = data['房屋租金']
rent_level = ["2000以下","2000-5000",'5000-8000',"8000-11000",'11000-15000','15000-20000','20000以上']
a1 = 0
a2 = 0
a3 = 0
a4 = 0
a5 = 0
a6 = 0
a7 = 0
for i in rent:
    if i <2000:
        a1 +=1
    if i >= 2000 and i<5000:
        a2 += 1
    if i>=5000 and i<8000:
        a3 += 1
    if i>=8000 and i<11000:
        a4+=1
    if i>=11000 and i<15000:
        a5+=1
    if i>=15000 and i<20000:
        a6 +=1
    if i>=20000:
        a7+=1
rent_list = [a1,a2,a3,a4,a5,a6,a7]
rent_pie = Pie("租金统计", title_pos='left', width=700, title_text_size=20)
rent_pie.add('租金',rent_level,rent_list,is_legend_show=False, is_label_show=True,rosetype='area')
rent_pie.render()

#建造年代饼图
year = data['建造年份']
year_level = ["1990以下","1990-1995",'1995-2000',"2000-2005",'2005-2010','2010-至今']
y1 = 0
y2 = 0
y3 = 0
y4 = 0
y5 = 0
y6 = 0
for i in year:
    if i <1990:
        y1 +=1
    if i >= 1990 and i<1995:
        y2 += 1
    if i>=1995 and i<2000:
        y3 += 1
    if i>=2000 and i<2005:
        y4+=1
    if i>=2005 and i<2010:
        y5+=1
    if i>=2010:
        y6 +=1
year_list = [y1,y2,y3,y4,y5,y6]
year_pie = Pie("建造年份统计", title_pos='left', width=700, title_text_size=20)
year_pie.add('年份',year_level,year_list,is_legend_show=False, is_label_show=True,rosetype='area')
year_pie.render()


#词云
room = data['房屋类型']
IsDuplicated = room.duplicated()
room_t = room.drop_duplicates()
room_list = []
room_type_num = []
for i in room_t:
    room_list.append(i)
    room_type_num.append(len(data[ data['房屋类型']==i]))
room_wordcloud = WordCloud(width=1400, height=800)
room_wordcloud.add("", room_list, room_type_num)
room_wordcloud.render()
