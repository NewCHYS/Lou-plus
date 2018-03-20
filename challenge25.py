# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas import DataFrame


def co2():

    # 1. 读取Data表和Country表的内容，筛选Data表中CO2E.KT部分数据
    Data = pd.read_excel("ClimateChange.xlsx", sheetname='Data')
    Country = pd.read_excel("ClimateChange.xlsx", sheetname='Country')
    Data2 = Data[Data['Series code']=='EN.ATM.CO2E.KT']
    # print(Data2)

    # 2. Data表删除无用列，空值转换，设置Country name为Index，填充数据，删除空数据行，计算总和
    Data2 = Data2.drop(['Country code','Series code','Series name','SCALE','Decimals'], axis=1)
    # print(Data2)
    Data2 = Data2.replace('..', np.nan)
    Data2.set_index('Country name', inplace=True)
    Data2 = Data2.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    Data2 = Data2.dropna()
    Data3 = Data2.sum(axis=1)
    # print(Data3)

    # 3. Country表筛选列，设置Country name为index，与Data表合并，得新Data表Data4，并将Country name转换回列
    Country = Country.loc[:, ['Country name', 'Income group']]
    Country.set_index('Country name', inplace=True)
    # print(Country)
    Data4 = pd.concat([Country, Data3], axis=1, join='inner')
    Data4.rename(columns={0:'sum'}, inplace=True)
    Data4 = Data4.reset_index()
    # print(Data4)
    
    # 4. 新建Dataframe表，按要求设置行、列名
    index = ['High income: OECD', 'High income: nonOECD', 'Low income', 'Lower middle income', 'Upper middle income']
    columns = ['Income group', 'Sum emissions', 'Highest emission country', 'Highest emissions', 'Lowest emission country', 'Lowest emissions']
    Dataframe = DataFrame(columns=columns)
    Dataframe['Income group'] = index
    Dataframe.set_index('Income group', inplace=True)
    # print(Dataframe)

    # 5. Data4表分组计算，将结果写入Dataframe表
    Data_sum = Data4.groupby(Data4['Income group']).sum()
    # print(Data_sum)
    for i in Data_sum.index:
        # print(Data_sum.loc[i, 'sum'])
        Dataframe.loc[i, 'Sum emissions'] = Data_sum.loc[i, 'sum']
    # print(Dataframe)
    Data_max = Data4.groupby(Data4['Income group']).max()
    # print(Data_max)
    for i in Data_max.index:
        Dataframe.loc[i, 'Highest emission country'] = Data_max.loc[i, 'Country name']
        Dataframe.loc[i, 'Highest emissions'] = Data_max.loc[i, 'sum']
    # print(Dataframe)
    Data_min = Data4.groupby(Data4['Income group']).min()
    # print(Data_min)
    for i in Data_min.index:
        Dataframe.loc[i, 'Lowest emission country'] = Data_min.loc[i, 'Country name']
        Dataframe.loc[i, 'Lowest emissions'] = Data_min.loc[i, 'sum']
    # print(Dataframe)
    print(str(Dataframe.loc[Dataframe.index[1], Dataframe.columns[4]]))
    return Dataframe


if __name__ == '__main__':
    print(co2())

