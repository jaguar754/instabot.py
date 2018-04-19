#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


class UserInfo:
    '''
    This class try to take some user info (following, followers, etc.)
    '''
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    url_user_info = "https://www.instagram.com/%s/"
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    url_list = {
        "ink361": {
            "main": "http://ink361.com/",
            "user": "http://ink361.com/app/users/%s",
            "search_name": "https://data.ink361.com/v1/users/search?q=%s",
            "search_id": "https://data.ink361.com/v1/users/ig-%s",
            "followers": "https://data.ink361.com/v1/users/ig-%s/followed-by",
            "following": "https://data.ink361.com/v1/users/ig-%s/follows",
            "stat": "http://ink361.com/app/users/ig-%s/%s/stats"
        }
    }

    def __init__(self, info_aggregator="ink361"):
        self.i_a = info_aggregator
        self.hello()

    def hello(self):
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': self.user_agent})
        main = self.s.get(self.url_list[self.i_a]["main"])
        if main.status_code == 200:
            return True
        return False

    def get_user_id_by_login(self, user_name):
        url_info = self.url_user_info % (user_name)
        info = self.s.get(url_info)
        all_data = info.text[info.text.find('javascript">window._sharedData'):]
        id_user = int(all_data[all_data.find('"profilePage_')+13 : all_data.find('"',all_data.find('"profilePage_')+13)])
        return id_user

    def get_user_by_media(self, media):
        '''
        Search user_name, if you don't have it.
        '''
        # just id
        search_media = self.url_media_detail % media
        x = self.s.get(search_media)
        if x.status_code == 200:
            r = json.loads(x.text)
            cUserName = r["graphql"]["shortcode_media"]["owner"]["username"]

            return cUserName
        return "Error in get_user_by_media"

    def get_followers(self, limit=-1):
        self.followers = None
        self.followers = []
        if self.user_id:
            next_url = self.url_list[self.i_a]["followers"] % self.user_id
            while True:
                followers = self.s.get(next_url)
                r = json.loads(followers.text)
                for u in r["data"]:
                    if limit > 0 or limit < 0:
                        self.followers.append({
                            "username": u["username"],
                            #"profile_picture": u["profile_picture"],
                            "id": u["id"].split("-")[1],
                            #"full_name": u["full_name"]
                        })
                        limit -= 1
                    else:
                        return True
                if r["pagination"]["next_url"]:
                    # have more data
                    next_url = r["pagination"]["next_url"]
                else:
                    # end of data
                    return True
        return False

    def get_following(self, limit=-1):
        self.following = None
        self.following = []
        if self.user_id:
            next_url = self.url_list[self.i_a]["following"] % self.user_id
            while True:
                following = self.s.get(next_url)
                r = json.loads(following.text)
                for u in r["data"]:
                    if limit > 0 or limit < 0:
                        self.following.append({
                            "username": u["username"],
                            #"profile_picture": u["profile_picture"],
                            "id": u["id"].split("-")[1],
                            #"full_name": u["full_name"]
                        })
                        limit -= 1
                    else:
                        return True
                if r["pagination"]["next_url"]:
                    # have more data
                    next_url = r["pagination"]["next_url"]
                else:
                    # end of data
                    return True
        return False

    def get_stat(self, limit):
        # todo
        return False


'''
# example
ui = UserInfo()
# search by user_name:
ui.search_user(user_name="danbilzerian")
# or if you know user_id ui.search_user(user_id="50417061")
print(ui.user_name)
print(ui.user_id)

# get following list with no limit
ui.get_following()
print(ui.following)

# get followers list with limit 10
ui.get_followers(limit=10)
print(ui.followers)
'''
