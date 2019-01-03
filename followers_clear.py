#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import concurrent.futures
from twitter import TwitterError
from api import api,confirm

follower_ids_cursor = -1
follower_ids = []
follower_ls = []

check_protected = confirm(
    'Do you deal with those who are protected and not tweeted?', default=True)

# 拿到自己的 followers
print('Getting followers list')
while follower_ids_cursor != 0:
    follower_ids_cursor, _, ids = api.GetFollowersPaged(
        cursor=follower_ids_cursor)
    follower_ls += ids
print('You have %d followers' % len(follower_ls))

no_mutual_followers = []

print('Getting zero or default profile image user info')
for user_info in follower_ls:
    follower_ids.append(user_info.id)
    try:
        need_mutu = False
        # user_info = api.GetUser(user_id=user_id)

        # 有发言过的，跳过
        if user_info.statuses_count == 0:
            need_mutu = True

        # 默认头像的，直接加进来
        if user_info.default_profile_image == True:
            need_mutu = True

        # 锁推&关注了我&没有被我关注
        if check_protected:
            if user_info.protected == True:
                if user_info.status == None:
                    need_mutu = True

        if need_mutu == False:
            continue

        # 加到需要 B 的队列中
        print(user_info.id, user_info.screen_name, user_info.name,
              user_info.default_profile_image, user_info.statuses_count)
        no_mutual_followers.append(user_info.id)

    except TwitterError as e:
        print(e)
        break
    except Exception as e:
        print(e)

print('You have %d followers is zero or default profile image user.' %
      len(no_mutual_followers))

# 记录下这些垃圾帐号的ID
with open('zero_ids.list', 'w') as f:
    for user_id in no_mutual_followers:
        f.write('%d\n' % user_id)

unblock = confirm(
    'Unblock those users after removed from followers list?', default=True)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

cancelled = False

block_failed_ids = []
unblock_failed_ids = []


def remove_follower(uid):
    if cancelled:
        return
    try:
        # B掉
        print('blocking %d' % uid)
        api.CreateBlock(uid)
    except TwitterError:
        block_failed_ids.append(uid)
    if unblock:
        try:
            # 解除 B
            print('unblocking %d' % uid)
            api.DestroyBlock(uid)
        except TwitterError:
            unblock_failed_ids.append(uid)


try:
    for user_id in no_mutual_followers:
        executor.submit(remove_follower, user_id)
    executor.shutdown(wait=True)
except (KeyboardInterrupt, SystemExit):
    cancelled = True
    print('Interrupted, exiting...')

with open('block_failed_ids.list', 'w') as f:
    for user_id in block_failed_ids:
        f.write('%d\n' % user_id)

with open('unblock_failed_ids.list', 'w') as f:
    for user_id in unblock_failed_ids:
        f.write('%d\n' % user_id)
