# !/usr/bin/env python3
# -  *  - coding:UTF-8 -  *  -

import time
import concurrent.futures
from twitter import TwitterError
from api import api, confirm, load_myself


myself = load_myself()
print(myself)
print(myself.id)

# res_post = api.PostUpdate("test")
# print(res_post)
# res_del = api.DestroyStatus(res_post.id)
# print(res_post)
# print(res_post.user.id, res_post.user.screen_name)

# print(api.GetSearch(term="from:vido_sun1 until:2018-01-01"))
