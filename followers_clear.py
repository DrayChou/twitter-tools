#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import concurrent.futures
from twitter import TwitterError
from api import api, confirm

# 配置文件
config = dict({
    # 是否删除那些跟随我而我没有跟随的账号
    # Do you deal with protected users who follow me but I don't follow?
    "check_protected"      : False,

    # 少于多少推的处理
    # delete if less than
    "less_statuses_count"  : 10,

    # 少于多少个关注着的处理
    # delete if less than
    "less_followers_count" : 10,

    # 是否处理默认头像的账号
    # delete if default profile image
    "default_profile_image": True,

    # 处理这些账号之后是否解除对他们的封锁
    # Unblock those users after removed from followers list?
    "unblock"              : True,

    # 白名单账号
    # whitelist
    "white_list"           : []
})

follower_ids_cursor = -1
follower_ids = []
follower_ls = []

# 拿到自己的 followers
print('Getting followers list')
while follower_ids_cursor != 0:
    follower_ids_cursor, _, ids = api.GetFollowersPaged(
        cursor=follower_ids_cursor)
    follower_ls += ids
print('You have %d followers' % len(follower_ls))

# 需要清理的账号
no_mutual_followers = []
white_list = config.get("white_list", [])
print('Getting zero or default profile image user info')
for user_info in follower_ls:
    follower_ids.append(user_info.id)
    try:
        need_mutu = False
        # user_info = api.GetUser(user_id=user_id)

        # 白名单
        if user_info.id in white_list or user_info.screen_name in white_list:
            continue

        # 少于多少推的处理，处理
        if user_info.statuses_count <= config.get("less_statuses_count", 0):
            need_mutu = True

        # 少于多少个关注着的处理，处理
        if user_info.followers_count <= config.get("less_followers_count", 0):
            need_mutu = True

        # 默认头像的，处理
        if config.get("default_profile_image", True):
            if user_info.default_profile_image == True:
                need_mutu = True

        # 锁推&关注了我&没有被我关注
        if config.get("check_protected", False):
            if user_info.protected == True:
                if user_info.status == None:
                    need_mutu = True

        if need_mutu == False:
            continue

        # 加到需要 B 的队列中
        print(
            user_info.id, user_info.screen_name, user_info.name, "\t\t\t",
            "protected:", user_info.protected,
            "default_profile_image:", user_info.default_profile_image,
            "statuses_count:", user_info.statuses_count,
            "followers_count:", user_info.followers_count
        )
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
    if config.get("unblock", True):
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
