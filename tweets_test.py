# !/usr/bin/env python3
# -  *  - coding:UTF-8 -  *  -

import time
import concurrent.futures
from twitter import TwitterError
from api import api, confirm


print(api.GetSearch(raw_query="f=tweets&q=from%3Avido_sun1%20until%3A2018-01-01"))
