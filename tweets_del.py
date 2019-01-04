# !/usr/bin/env python3
# -  *  - coding:UTF-8 -  *  -

import time
import concurrent.futures
from twitter import TwitterError
from api import api, confirm

# 搜索删除
list = api.GetSearch(term = "#taichibot", since_id = 0)
for tweet in list:
    print(tweet)
    api.DestroyStatus(tweet.id)

# 直接根据 id 删除
id_list = [
    "707446814979584004",
]
for ids in id_list:
    res = api.DestroyStatus(ids)
    print(ids, res)