# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import time


def co2_gdp_plot():

    # 1. 读取Data表的内容，筛选Data表中CO2和GDP部分数据
    Data = pd.read_excel("ClimateChange.xlsx", sheetname='Data')
    Data_CO2 = Data[Data['Series code']=='EN.ATM.CO2E.KT']
    Data_GDP = Data[Data['Series code']=='NY.GDP.MKTP.CD']
    # print(Data)

    # 2. 两个Data表删除无用列，设置Country code为Index，填充数据，计算总和
    Data_CO2 = Data_CO2.drop(['Country name','Series code','Series name','SCALE','Decimals'], axis=1)
    Data_GDP = Data_GDP.drop(['Country name','Series code','Series name','SCALE','Decimals'], axis=1)
    # print(Data)
    Data_CO2.set_index('Country code', inplace=True)
    Data_GDP.set_index('Country code', inplace=True)
    Data_CO2 = Data_CO2.replace('..', 0)
    Data_GDP = Data_GDP.replace('..', 0)
    Data_CO2 = Data_CO2.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    Data_GDP = Data_GDP.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    Data_CO2 = Data_CO2.sum(axis=1)
    Data_GDP = Data_GDP.sum(axis=1)
    # print(Data_CO2)
    # print(Data_GDP)

    # 3. 两个Data表合并，便于操作，取每列最大值和最小值，进行归一化处理 
    Data = pd.DataFrame({'CO2':Data_CO2, 'GDP':Data_GDP})
    # print(Data)
    Max_CO2, Min_CO2 = Data['CO2'].max(), Data['CO2'].min()
    # print(Max_CO2, Min_CO2)
    Max_GDP, Min_GDP = Data['GDP'].max(), Data['GDP'].min()
    # print(Max_GDP, Min_GDP)
    n_CO2 = Max_CO2 - Min_CO2
    n_GDP = Max_GDP - Min_GDP
    for i in range(0, len(Data)):
        Data.iloc[i,0] = (Data.iloc[i,0]-Min_CO2)/n_CO2 if Data.iloc[i,0] != 0 else 0
        Data.iloc[i,1] = (Data.iloc[i,1]-Min_GDP)/n_GDP if Data.iloc[i,0] != 0 else 0
    # print(Data)

    # 4 绘图
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('GDP-CO2')
    ax.set_xlabel('Countries')
    ax.set_ylabel('Values')
    index_x = list(Data.index)
    labels = ['CHN','USA','GBR','FRA','RUS']
    ax.plot(index_x, list(Data['CO2']))
    ax.plot(index_x, list(Data['GDP']))
    # ax.set_xticks(index_x)
    plt.xticks(labels, labels, rotation='vertical')
    plt.legend(('CO2-SUM','GDP-SUM'), shadow=False, loc=(0.01,0.85))

    #fig = plt.subplot()

    # 5 返回需要的数据
    n1 = float(('%.3f' % Data.loc['CHN','CO2']))
    # print(n1)
    n2 = float(('%.3f' % Data.loc['CHN','GDP']))
    # print(n2)
    # china = [Data.loc['CHN','CO2'].round(3), Data.loc['CHN','GDP'].round(3)]
    china = [n1, n2]
    # print(china)
    return fig, china


if __name__ == '__main__':
    fig, china = co2_gdp_plot()
    print(china)
    fig.show()
    time.sleep(10)
