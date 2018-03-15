import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import json


def analysis():
    file = 'user_study.json'

    try:
        data = pd.read_json(file)
    except:
        return 0, 0
    
    data2 = data.groupby('user_id').sum()
#    print(data2)
    userid_list = data2.index
    print(userid_list)
    times_list = data2.minutes
    print(times_list)
    print(type(userid_list))
    return userid_list, times_list


def data_plot():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.set_title("Study Data")
    ax.set_xlabel("User ID")
    ax.set_ylabel("Study Time")

#    min_user_id = 0
#    max_user_id = 200000
#    x = np.arange(min_user_id, max_user_id+1, (max_user_id - min_user_id)/5)
#    y = np.arange(0, 3001, 500)
#    ax.set_xticks(x)
#    ax.set_yticks(y)
    
    x_data, y_data = analysis()
    ax.plot(x_data, y_data)
    plt.show()
    return ax


if __name__ == '__main__':
    data_plot()
#    analysis()
