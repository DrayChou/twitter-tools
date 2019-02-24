#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import twitter
from twitter import TwitterError
from requests_oauthlib import OAuth1Session
import webbrowser
import yaml

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'


def confirm(message, default=None):
    if default is None:
        t = input(message)
    else:
        if default == True or default == False:
            if default:
                default_input = 'y'
            else:
                default_input = 'n'
        else:
            default_input = default

        t = input('%s [%s]' % (message, default_input))
    if t == '' or t is None and default is not None:
        return default
    while t != 'y' and t != 'n':
        return t
    if t == 'y':
        return True
    else:
        return False


def get_access_token(ck, cs):
    oauth_client = OAuth1Session(
        client_key=ck, client_secret=cs, callback_uri='oob')

    print('\nRequesting temp token from Twitter...\n')

    try:
        resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(
            e)

    url = oauth_client.authorization_url(AUTHORIZATION_URL)

    print('I will try to start a browser to visit the following Twitter page '
          'if a browser will not start, copy the URL to your browser '
          'and retrieve the pincode to be used '
          'in the next step to obtaining an Authentication Token: \n'
          '\n\t{0}'.format(url))

    webbrowser.open(url)
    pincode = input('\nEnter your pincode? ')

    print('\nGenerating and signing request for an access token...\n')

    oauth_client = OAuth1Session(
        client_key=ck, client_secret=cs,
        resource_owner_key=resp.get('oauth_token'),
        resource_owner_secret=resp.get('oauth_token_secret'),
        verifier=pincode
    )
    try:
        resp = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(
            e)

    return resp.get('oauth_token'), resp.get('oauth_token_secret')


def load_credentials():
    try:
        with open('.twitter_credentials.yml') as f:
            c = yaml.load(f)
            return c['access_token'], c['access_token_secret'], c.get("user")
    except IOError:
        return None


def load_myself():
    try:
        with open('.twitter_credentials.yml') as f:
            c = yaml.load(f)
            return c.get("user")
    except IOError:
        return None


def load_consumer():
    try:
        with open('.twitter_consumer.yml') as f:
            c = yaml.load(f)
            return c['consumer_key'], c['consumer_secret']
    except IOError:
        return None


def get_credentials(ck, cs):
    if confirm('Do you have access token and secret already?', default=False):
        at = input('Input access token: ').strip()
        ats = input('Input access token secret: ').strip()
    else:
        at, ats = get_access_token(ck, cs)
    return at, ats


def get_consumer():
    ck = confirm('Input consumer key: ', '').strip()
    cs = confirm('Input consumer secret: ', '').strip()
    return ck, cs,


def get_myself():
    res_post = api.PostUpdate("test")
    res_del = api.DestroyStatus(res_post.id)

    return res_post.user


# Create ArgumentParser() object
parser = argparse.ArgumentParser()
# Add argument
parser.add_argument('--new_user', required=False, type=int, default=0,
                    help="Do you want to switch to a new user?")
# Parse argument
args = parser.parse_args()

consumer = load_consumer()
credentials = load_credentials()

if not consumer or (args.new_user != -1 and confirm('Do you want to switch to a new consumer?', default=False)):
    credentials = None
    consumer = get_consumer()
    with open(".twitter_consumer.yml", "w") as f:
        yaml.dump({
            'consumer_key': consumer[0],
            'consumer_secret': consumer[1],
        }, f, default_flow_style=False)

is_new_credentials = False
if not credentials or (args.new_user != -1 and confirm('Do you want to switch to a new user?', default=False)):
    is_new_credentials = True
    credentials = get_credentials(consumer[0], consumer[1])

api = twitter.Api(
    consumer_key=consumer[0], consumer_secret=consumer[1],
    access_token_key=credentials[0], access_token_secret=credentials[1]
)

# 拿到自己的信息
if is_new_credentials:
    myself = get_myself()
    with open('.twitter_credentials.yml', 'w') as f:
        yaml.dump({
            'access_token': credentials[0],
            'access_token_secret': credentials[1],
            'user': myself,
        }, f, default_flow_style=False)

if __name__ == '__main__':
    follower_ids_cursor, _, ids = api.GetFollowersPaged(count=10)
    for user_info in ids:
        # print(user_info)
        # 锁推&关注了我&没有被我关注
        if user_info.protected == True:
            print('protected one info', user_info, user_info.status)
            if user_info.status == None:
                print('not follow me:', user_info.id,
                      user_info.screen_name, user_info.name)
