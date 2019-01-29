# !/usr/bin/env python3
# -  *  - coding:UTF-8 -  *  -

import time
import concurrent.futures
from twitter import TwitterError
from api import api, confirm

id_list = [
]

# 搜索删除`````````````````
list = api.GetSearch(raw_query="from:vido_sun1 until:2018-01-01", since_id=0)
for tweet in list:
    id_list.append(tweet.id)
    # print(tweet)

# 直接根据 id 删除
for ids in id_list:
    try:
        res = api.GetStatus(ids)
        print(res.id, res.created_at, res.text, res.media)
        # res = api.DestroyStatus(ids)
        # print(ids, res)
    except Exception as ex:
        print(ids, ex)
