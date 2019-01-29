# !/usr/bin/env python3
# -  *  - coding:UTF-8 -  *  -

import time
import concurrent.futures
from twitter import TwitterError
from api import api, confirm


print(api.GetSearch(term="from:vido_sun1 until:2018-01-01"))