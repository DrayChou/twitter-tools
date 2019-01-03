#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time
import concurrent.futures
from twitter import TwitterError
from api import api, confirm

# Delete own tweets
owned_status = api.GetUserTimeline(count=200)
num_owned_status = 0
while(len(owned_status) > 0):
    for s in owned_status:
        api.DestroyStatus(s.id)
        print('One tweet deleted', s.id)
        num_owned_status += 1
    owned_status = api.GetUserTimeline(count=200)
    time.sleep(2)

print('Your ' + str(num_owned_status) + ' tweets has been deleted.')


# Delete retweets
owned_retweets = api.GetUserRetweets(count=200)
num_owned_retweets = 0
while(len(owned_retweets) > 0):
    for s in owned_retweets:
        api.DestroyStatus(s.id)
        print('One retweet deleted', s.id)
        num_owned_retweets += 1
    owned_retweets = api.GetUserRetweets(count=200)
    time.sleep(2)

print('Your ' + str(num_owned_retweets) + ' retweets has been deleted.')


# Delete replies
owned_replies = api.GetReplies(count=200)
num_owned_replies = 0
while(len(owned_replies) > 0):
    for s in owned_replies:
        api.DestroyStatus(s.id)
        print('One reply deleted', s.id)
        num_owned_replies += 1
    owned_replies = api.GetReplies(count=200)
    time.sleep(2)

print('Your ' + str(num_owned_replies) + ' replies has been deleted.')
