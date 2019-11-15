# !/usr/bin/env python3
# -  *  - coding:UTF-8 -  *  -

import time
import concurrent.futures
from twitter import TwitterError
from api import api, confirm

# # 搜索删除`````````````````
# list = api.GetSearch(raw_query="from:vido_sun1 until:2018-01-01", since_id=0)
# for tweet in list:
#     id_list.append(tweet.id)
#     # print(tweet)

# 直接根据 id 删除

f = open("ids.txt")
line = f.readline()
while line:
    line = f.readline()
    try:
        ids = line.strip()
        if len(ids) < 1:
            continue

        # res = api.GetStatus(ids)
        # print(res.id, res.created_at, res.text, res.media)
        res = api.DestroyStatus(ids)
        print(ids, res)
    except Exception as ex:
        print(line, ex)
f.close()

# export http_proxy=http://127.0.0.1:1080
# export https_proxy=http://127.0.0.1:1080