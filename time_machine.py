# !/usr/bin/env python3
# -  *  - coding:UTF-8 -  *  -

import time
import random
import concurrent.futures
from twitter import TwitterError
from api import api, confirm

from time_machine_setting import twid, twtag, action_dict

last_tweet_time = 0
term = "-#{} from:{}".format(twtag, twid)
tweet_list = api.GetSearch(term=term, count=10)
if len(tweet_list) > 0:
    t_t = time.strptime(tweet_list[0].created_at, '%a %b %d %H:%M:%S %z %Y')
    last_tweet_time = time.mktime(t_t) - time.timezone
    # print(t_t, last_tweet_time, time.timezone, time.tzname)
print(term, tweet_list, last_tweet_time)

# 是否发出去了
# tweed = False
# for sc, action_ls in action_dict.items():
#     if tweed:
#         break
#     if time.time() - last_tweet_time > sc:
#         for action in action_ls:
#             if action[0]():
#                 msg_ls = action[1]
#                 msg = msg_ls[random.randint(0, len(msg_ls)-1)]
#                 msg = "#{} {}".format(twtag, msg)
#                 res = api.PostUpdate(msg)
#                 if res:
#                     print(msg, "\n", res)
#                     tweed = True
#                     break
#                 else:
#                     print(msg, res)
#                     pass
#             else:
#                 # print(action)
#                 pass
