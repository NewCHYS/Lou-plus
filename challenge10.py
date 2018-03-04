# -*- coding: utf-8 -*-


import sys
from pymongo import MongoClient


def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    res = list(contests.aggregate([{'$match':{'user_id':user_id}},{'$group':{'_id':"$user_id",'scores':{'$sum':"$score"},'total_time':{'$sum':"$submit_time"}}}]))
    if len(res) == 0:
        return 0, 0, 0
    data = res[0]
    pipe = [
            {
                '$group':{
                    '_id': '$user_id',
                    'total_score':{'$sum':'$score'},
                    'total_time':{'$sum':'$submit_time'}
                }
            },
            {
                '$match':{
                    '$or':[
                        {'total_score': {'$gt':data['scores']}},
                        {
                            'total_score': {'$eq':data['scores']},
                            'total_time': {'$lt':data['total_time']}
                        }
                    ]
                }
            },
            {'$group':{'_id':None, 'count': {'$sum':1}}}
        ]

    res2 = list(contests.aggregate(pipe))

    if len(res2) > 0:
        rank = res2[0]['count'] + 1
    else:
        rank = 1

    score = data['scores']
    submit_time = data['total_time']
    return rank, score, submit_time 


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise()
        user_id = int(sys.argv[1])
    except:
        print("Parameter Error")
        sys.exit(1)
    userdata = get_rank(user_id)
    print(userdata)


