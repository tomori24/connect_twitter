# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
import sys
import datetime
import pandas as pd

class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.api = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

    def get_tweet_users(self, word, count=5, result_type='recent', 
                        until=str(datetime.date.today()), url="https://api.twitter.com/1.1/search/tweets.json"):
        params ={'q': word, 'count': count, 'result_type': result_type, 'until': until}
        users_list = []
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            search_timeline = json.loads(req.text)
            for tweet in search_timeline['statuses']:
                print('---------------------------------')
                print('{} \n{}'.format(tweet['user']['screen_name'], tweet['text']))
                print('---------------------------------')
                user_dict = {}
                user_dict['id'] = tweet['user']['id']
                user_dict['screen_name'] = tweet['user']['screen_name']
                user_dict['followers_count'] = tweet['user']['followers_count']
                user_dict['friends_count'] = tweet['user']['friends_count']
                users_list.append(user_dict)
            users_list = list(map(json.loads, set(map(json.dumps, users_list))))
            return users_list
        else:
            print("ERROR: %d" % req.status_code)
            return []

    # count <= 5000
    def get_followers_id(self, id, count=5, url='https://api.twitter.com/1.1/followers/ids.json'):
        params = {'user_id': id, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            followers_list = req.json()['ids']
            return followers_list
        else: 
            print("ERROR: %d" % req.status_code)
            return []

    # scn = screen name, count <= 200
    def get_followers_info(self, id, count=5, url='https://api.twitter.com/1.1/followers/list.json'):
        params = {'user_id': id, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            users_list = []
            for user in req.json()['users']:
                user_dict = {}
                user_dict['id'] = user['id']
                user_dict['screen_name'] = user['screen_name']
                user_dict['followers_count'] = user['followers_count']
                user_dict['friends_count'] = user['friends_count']
                users_list.append(user_dict)
            return users_list
        else: 
            print("ERROR: %d" % req.status_code)
            return []

    # count <= 5000
    def get_friends_id(self, id, count=5, url='https://api.twitter.com/1.1/friends/ids.json'):
        params = {'user_id': id, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            following_list = req.json()['ids']
            return following_list
        else: 
            print("ERROR: %d" % req.status_code)
            return []

    # scn = screen name, count <= 200
    def get_friends_info(self, id, count=200, url='https://api.twitter.com/1.1/friends/list.json'):
        params = {'user_id': id, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            users_list = []
            for user in req.json()['users']:
                user_dict = {}
                user_dict['id'] = user['id']
                user_dict['screen_name'] = user['screen_name']
                user_dict['followers_count'] = user['followers_count']
                user_dict['friends_count'] = user['friends_count']
                users_list.append(user_dict)
            return users_list
        else: 
            print("ERROR: %d" % req.status_code)
            return []

    def get_users_info(self, id=None, scn=None, url='https://api.twitter.com/1.1/users/lookup.json'):
        if id is None and scn is None:
            return {}
        params = {'user_id': id, 'screen_name': scn}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            users_list = []
            for user in req.json():
                user_dict = {}
                user_dict['id'] = user['id']
                user_dict['screen_name'] = user['screen_name']
                user_dict['followers_count'] = user['followers_count']
                user_dict['friends_count'] = user['friends_count']
                users_list.append(user_dict)
            if len(users_list) == 1:
                return users_list[0]
            return users_list
        else:
            print("ERROR: %d" % req.status_code)
            return []

    def get_timeline(self, since_id='', url='https://api.twitter.com/1.1/statuses/home_timeline.json'):
        params = {'count': 100, 'since_id': since_id, 'trim_user': 'false', 'include_entities': 'false'}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            timeline_dict = {}
            for tweet in req.json():
                timeline_dict[tweet[id]] = tweet['text']
            return timeline_dict