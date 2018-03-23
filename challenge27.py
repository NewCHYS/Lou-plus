# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def climate_plot():

    # 1. 读取两个表的内容，筛选Data表中所有温室气体部分数据，去掉无用列，只保留年度数据
    #    Temp表读取数据，去掉无用列，设置时间Index
    Data = pd.read_excel("ClimateChange.xlsx", sheetname='Data')
    n = ['EN.ATM.CO2E.KT', 'EN.ATM.METH.KT.CE', 'EN.ATM.NOXE.KT.CE', 'EN.ATM.GHGO.KT.CE', 'EN.CLC.GHGR.MT.CE']
    Data = Data[Data['Series code'].isin(n)]
    Data = Data.drop(['Country code', 'Country name','Series code','Series name','SCALE','Decimals'], axis=1)
    # print(Data)
    # print(t)

    Temp = pd.read_excel("GlobalTemperature.xlsx")
    Temp = Temp.drop(['Land Max Temperature', 'Land Min Temperature'], axis=1)
    index = pd.to_datetime(Temp.pop('Date'))
    # print(index)
    Temp = Temp.set_index(index)
    # print(Temp)
    # print(t)

    # 2. 图1、图2数据获取
    #    Data表，填充数据，去掉空值行，去掉2011年一列，计算各列总和，归一化处理
    #    Temp表取年度1990至2010期间数据，数据填充，去除空值行，按年度计算，归一化处理
    # print(Data)
    Data = Data.replace('..', np.nan)
    Data = Data.drop(2011, axis=1)
    Data = Data.dropna(how='all')
    Data = Data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    # print(Data)
    Data = Data.sum()
    # print(Data)
    Max = Data.max()
    Min = Data.min()
    n = Max - Min
    Data = (Data - Min) / n
    # Data = Data.drop(2011)
    # print(Data)
    # print(t)
    
    Temp12 = Temp['1990':'2010']
    Temp12 = Temp12.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1).dropna()
    Temp12 = Temp12.resample('12m', closed='left').sum()
    # print(Temp12)
    # print(t)
    Max = Temp12.max()
    Min = Temp12.min()
    n = Max - Min
    Temp12 = (Temp12 - Min) / n
    # print(Temp12)
    # print(t)

    # 3. 图1、图2绘制
    fig = plt.subplot(2,2,1, facecolor='lightgray')
    plt.grid(True, color='white', zorder=0)
    fig.set_xlabel('Years')
    fig.set_ylabel('Values')
    fig.plot(Data.index, list(Temp12['Land Average Temperature']), color='blue', zorder=10)
    fig.plot(Data.index, list(Temp12['Land And Ocean Average Temperature']), color='green', zorder=10)
    fig.plot(Data.index, list(Data), color='red', zorder=10)
    fig.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    # x = [1990,1992,1995,1997,2000,2002,2005,2007,2010]
    # plt.xticks(x, map(str,x))
    plt.legend(('Land Average Tempterature','Land And Ocean Average Temperature','Totla GHG'), shadow=False, loc='best')
    # plt.show()
    # print(t)

    fig = plt.subplot(2,2,2, facecolor='lightgray')
    plt.grid(True, color='white', zorder=0)
    fig.set_xlabel('Years')
    fig.set_ylabel('Values')
    index_x = list(Data.index)
    fig.bar(Data.index, list(Temp12['Land Average Temperature']), width=0.2, color='blue', zorder=10)
    fig.bar(Data.index+0.2, list(Temp12['Land And Ocean Average Temperature']), width=0.2, color='green', zorder=10)
    fig.bar(Data.index+0.4, list(Data), width=0.2, color='red', zorder=10)
    plt.xticks(index_x, map(str, index_x), rotation='vertical')
    plt.legend(('Land Average Tempterature','Land And Ocean Average Temperature','Totla GHG'), shadow=False, loc='best')
    # plt.show()
    # print(t)

    # 4. 图3、图4数据获取
    Temp34 = Temp
    # Temp34 = Temp34.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1).dropna()
    # Temp34 = Temp34.dropna(how='all')
    Temp34 = Temp34.resample('Q').mean()
    # Temp34 = Temp34.dropna()
    # Temp34 = Temp34.replace(np.nan, 0)
    # print(Temp34)
    # print(t)

    # 5. 图3、图4绘制
    # fig = plt.figure()
    fig = plt.subplot(2,2,3)
    Temp34.plot(kind='area', ax=fig)
    fig.set_xlabel('Quarters')
    fig.set_ylabel('Temperature')

    fig = plt.subplot(2,2,4)
    Temp34.plot(kind='kde', ax=fig)
    fig.set_xlabel('Values')
    fig.set_ylabel('Values')
    # fig.stackplot(Temp34.index, list(Temp34['Land Average Temperature']), list(Temp34['Land And Ocean Average Temperature']))
    # plt.show()

    # 5 返回需要的数据
    
    return fig


if __name__ == '__main__':
    fig = climate_plot()
    plt.show()

