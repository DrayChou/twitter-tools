# !/usr/bin/env python3
# -  *  - coding:UTF-8 -  *  -

import time
import random
import concurrent.futures
from twitter import TwitterError
from api import api, confirm

from time_machine_setting import twid, more_than_time_msg

last_tweet_time = 0
tweet_list = api.GetUserTimeline(screen_name=twid, count=1)
if len(tweet_list) > 0:
    last_tweet_time = time.mktime(time.strptime(
        tweet_list[0].created_at, '%a %b %d %H:%M:%S %z %Y'))
print(tweet_list)

for sc, msg_ls in more_than_time_msg.items():
    if (time.time() - last_tweet_time > sc):
        msg = msg_ls[random.randint(0, len(msg_ls)-1)]
        res = api.PostUpdate(msg)
        print(res)
