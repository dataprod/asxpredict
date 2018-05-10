#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 23:16:27 2018

@author: stals
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
import csv
import math 

dataset = pd.read_csv('asx.csv')

values = dataset.values
sum_values = []


    

index_current = 0
for value in values[:,5]:
    number = value[0:len(value)-1]
    type_num = value[len(value)-1]
    
    if type_num == 'M':
        number = float(number) * 1000000
        
    elif type_num == 'B':
        number = float(number) * 1000000000
    else:
        number = np.mean(sum_values)
    
    values[index_current][5] = number
    sum_values.append(number)
    index_current+=1

#print(values[:,5])
   
index_current = 0

for date in values[:,0]:
    new_date = datetime.strptime(date, '%b %d, %Y')
    values[index_current][0] = new_date
    index_current+=1

for i in range(1,5):
    index_current = 0
    for number in values[:,i]:
        num_float = float(number)
        values[index_current][i] = num_float
        index_current+=1
#print(values[0])
values = values[::-1]
#print(values[0])

fake_dates =[]
index = 0
for day in values[:,0]:
    day_of_week = day.weekday()
    if day_of_week == 6:
        
        fake_dates.append(index)
    index+=1

values = np.delete(values[:,], fake_dates, 0)


onbv = [0,0]
time_counter = 2
time = [0 , 1]

index_current_volume = 1
index_close_tminus = 0
index_close_t = 1
num_downdays = 0
for volume in values[1:,5]:
    time.append(time_counter)
    time_counter+=1
    #volume for day t-1 = volume
    #vlume for day t = values[index_current_volume]
    #obv for t-1 = onbv[len(onbv)-2]
    #the volume calculated is meant to be the volume for day t+1
    
    #if close on day t i higher than t-1, onbv = obvt-1 + volume on day t
    #if close on day t is lower than t-1, onbv = obvt-1 -volume on day t
    
    on_balance_tminus = onbv[len(onbv)-1]
    close_tminus = values[index_close_tminus][1]
    close_t = values[index_close_t][1]
    volume_day_t = volume
    #print("onbv t-1 %f, closet-1 %f, closet %f, volume t %f"% (on_balance_tminus,close_tminus,close_t,volume_day_t) )
    
    if close_tminus > close_t:
        on_balance = on_balance_tminus - volume_day_t
        num_downdays+=1
    else:
        on_balance = on_balance_tminus + volume_day_t
        
    #print("new obv %f at time = %d" % (on_balance, index_close_t+1))
    onbv.append(on_balance)
    index_current_volume += 1
    index_close_tminus += 1
    index_close_t += 1

ma_5 = [0,0,0,0,0]
index = 5
for price in values[5:,1]:
    sum_5 = 0
    for day in range(index-5,index):
        sum_5 += values[day][1]
    avg = sum_5/5
    ma_5.append(avg)
    index+=1

ma_6 = [0,0,0,0,0,0]
index = 6
for price in values[6:,1]:
    sum_6 = 0
    for day in range(index-6,index):
        sum_6 += values[day][1]
    avg = sum_6/6
    ma_6.append(avg)
    index+=1
    
bias_6 = [0,0,0,0,0,0]
index = 6
for price in values[6:,1]:
    price_t = values[index][1]
    ma_6_t = ma_6[index]
    bias = ((price_t-ma_6_t)/ma_6_t)*100
    bias_6.append(bias)
    index+=1
    
psy_12 = [0,0,0,0,0,0,0,0,0,0,0,0]
index = 12
for price in values[12:,6]:
    sum_psy = 0
    for day in range(index-12,index):
        if values[day][6] > 0:
            sum_psy+=1
        
    a = (sum_psy/12)*100
    psy_12.append(a)
    index+=1
    
asy_5 = [0,0,0,0,0,0]
index = 6
for price in values[6:,1]:
    sy_num = 0
    for day in range(index-5,index):
        sy_num += (math.log(values[day][1])-math.log(values[day-1][1]))*100
        #print((math.log(values[day][1])-math.log(values[day-1][1]))*100)
    avg = sy_num/5
    #print("avg %f" % avg)
    asy_5.append(avg)
    index+=1

asy_4 = [0,0,0,0,0]
index = 5
for price in values[5:,1]:
    sy_num = 0
    for day in range(index-4,index):
        sy_num += (math.log(values[day][1])-math.log(values[day-1][1]))*100
        #print((math.log(values[day][1])-math.log(values[day-1][1]))*100)
    avg = sy_num/4
    #print("avg %f" % avg)
    asy_4.append(avg)
    index+=1 
    
asy_3 = [0,0,0,0]
index = 4
for price in values[4:,1]:
    sy_num = 0
    for day in range(index-3,index):
        sy_num += (math.log(values[day][1])-math.log(values[day-1][1]))*100
        #print((math.log(values[day][1])-math.log(values[day-1][1]))*100)
    avg = sy_num/3
    #print("avg %f" % avg)
    asy_3.append(avg)
    index+=1 

asy_2 = [0,0,0]
index = 3
for price in values[3:,1]:
    sy_num = 0
    for day in range(index-2,index):
        sy_num += (math.log(values[day][1])-math.log(values[day-1][1]))*100
        #print((math.log(values[day][1])-math.log(values[day-1][1]))*100)
    avg = sy_num/2
    #print("avg %f" % avg)
    asy_2.append(avg)
    index+=1 
    
asy_1 = [0,0]
index = 2
for price in values[2:,1]:
    sy_num = 0
    for day in range(index-1,index):
        sy_num += (math.log(values[day][1])-math.log(values[day-1][1]))*100
        #print((math.log(values[day][1])-math.log(values[day-1][1]))*100)
    avg = sy_num
    #print("avg %f" % avg)
    asy_1.append(avg)
    index+=1
    
weekdays = []
for day in values[:,0]:
    day_of_week = day.weekday()
    if day_of_week == 6:
        print(day)
    weekdays.append(day_of_week)

index = 0
for day in values[:,6]:
    percentage = day*100
    values[index][6] = "%.3f" % percentage
    index+=1
    

final_list = []
headings = ['Date','Close','Open','High','Low','Volume','OBV','BIAS_6','5_MA'
            ,'PSY_12','ASY_5','ASY_4','ASY_3','ASY_2','ASY_1','DAY','Change' ]
final_list.append(headings)

index = 0
for day in values[:,:]:
    row_array = []
    row_array.append(day[0].strftime("%d-%m-%Y"))
    for i in range(1,6):
        row_array.append(day[i])
    row_array.append(onbv[index])
    row_array.append(bias_6[index])
    row_array.append(ma_5[index])
    row_array.append(psy_12[index])
    row_array.append(asy_5[index])
    row_array.append(asy_4[index])
    row_array.append(asy_3[index])
    row_array.append(asy_2[index])
    row_array.append(asy_1[index])
    row_array.append(weekdays[index])
    row_array.append(day[6])
    index+=1
    final_list.append(row_array)


with open('final_data.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(final_list)




#print(onbv)
x = weekdays
y = asy_5[50:]
z = values[:,6]
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('date')
ax1.set_ylabel('asx200', color=color)
ax1.plot(z, x, color=color)
ax1.tick_params(axis='y', labelcolor=color)

'''
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('obv', color=color)  # we already handled the x-label with ax1
ax2.plot(x, y, color=color)
ax2.tick_params(axis='y', labelcolor=color)
'''
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

    
    
    

#print(values[0])











