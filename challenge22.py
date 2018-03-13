import json
import pandas as pd

def analysis(file, user_id):
    times = 0
    minutes = 0
    try:
        data = pd.read_json(file)
        data2 = data[data['user_id']==user_id]
    except:
        return 0

    minutes = data2.sum()['minutes']
#    print(minutes)
    times = data2.count()['minutes']
#    print(times)

    return times, minutes


if __name__ == '__main__':
    file = 'user_study.json'
    user_id = 5348
    print(analysis(file, user_id))
