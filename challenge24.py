import pandas as pd


def quarter_volume():
    second_volume = 0
    data = pd.read_csv('apple.csv', header=0)
#    print(data)
    data2 = data.loc[:,['Date', 'Volume']]
#    print(data2)
    iD = pd.to_datetime(data2.Date.tolist())
    data3 = pd.Series(data2.Volume.tolist(), index=iD)
#    print(data3)
    data4 = data3.resample('Q').sum()
#    print(data4)
    data5 = data4.sort_values(ascending=False)
#    print(data5)
    second_volume = data5[1]

    return second_volume


if __name__ == '__main__':
    print(quarter_volume())
