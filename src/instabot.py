#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from .unfollow_protocol import unfollow_protocol
from .userinfo import UserInfo
import atexit
import datetime
import itertools
import json
import logging
import random
import signal
import sys
import sqlite3
import time
import requests
from .sql_updates import check_and_update, check_already_liked, check_already_followed
from .sql_updates import insert_media, insert_username, insert_unfollow_count
from .sql_updates import get_usernames_first, get_usernames, get_username_random
from .sql_updates import check_and_insert_user_agent
from fake_useragent import UserAgent

class InstaBot:
    """
    Instagram bot v 1.2.0
    like_per_day=1000 - How many likes set bot in one day.

    media_max_like=0 - Don't like media (photo or video) if it have more than
    media_max_like likes.

    media_min_like=0 - Don't like media (photo or video) if it have less than
    media_min_like likes.

    tag_list = ['cat', 'car', 'dog'] - Tag list to like.

    max_like_for_one_tag=5 - Like 1 to max_like_for_one_tag times by row.

    log_mod = 0 - Log mod: log_mod = 0 log to console, log_mod = 1 log to file,
    log_mod = 2 no log.

    https://github.com/LevPasha/instabot.py
    """
    database_name = "follows_db.db"
    follows_db = None
    follows_db_c = None

    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_detail = 'https://www.instagram.com/%s/?__a=1'
    api_user_detail = 'https://i.instagram.com/api/v1/users/%s/info/'

    user_agent = "" ""
    accept_language = 'en-US,en;q=0.5'

    # If instagram ban you - query return 400 error.
    error_400 = 0
    # If you have 3 400 error in row - looks like you banned.
    error_400_to_ban = 3
    # If InstaBot think you are banned - going to sleep.
    ban_sleep_time = 2 * 60 * 60

    # All counter.
    bot_mode = 0
    like_counter = 0
    follow_counter = 0
    unfollow_counter = 0
    comments_counter = 0
    current_user = 'hajka'
    current_index = 0
    current_id = 'abcds'
    # List of user_id, that bot follow
    bot_follow_list = []
    user_info_list = []
    user_list = []
    ex_user_list = []
    unwanted_username_list = []
    is_checked = False
    is_selebgram = False
    is_fake_account = False
    is_active_user = False
    is_following = False
    is_follower = False
    is_rejected = False
    is_self_checking = False
    is_by_tag = False
    is_follower_number = 0

    self_following = 0
    self_follower = 0

    # Log setting.
    logging.basicConfig(filename='errors.log', level=logging.INFO)
    log_file_path = ''
    log_file = 0

    # Other.
    user_id = 0
    media_by_tag = 0
    media_on_feed = []
    media_by_user = []
    login_status = False

    # Running Times
    start_at_h = 0,
    start_at_m = 0,
    end_at_h = 23,
    end_at_m = 59,

    # For new_auto_mod
    next_iteration = {"Like": 0, "Follow": 0, "Unfollow": 0, "Comments": 0}

    def __init__(self,
                 login,
                 password,
                 like_per_day=1000,
                 media_max_like=50,
                 media_min_like=0,
                 follow_per_day=0,
                 follow_time=5 * 60 * 60,
                 unfollow_per_day=0,
                 start_at_h=0,
                 start_at_m=0,
                 end_at_h=23,
                 end_at_m=59,
                 database_name='follows_db.db',
                 comment_list=[["this", "the", "your"],
                               ["photo", "picture", "pic", "shot", "snapshot"],
                               ["is", "looks", "feels", "is really"],
                               ["great", "super", "good", "very good", "good",
                                "wow", "WOW", "cool", "GREAT", "magnificent",
                                "magical", "very cool", "stylish", "beautiful",
                                "so beautiful", "so stylish", "so professional",
                                "lovely", "so lovely", "very lovely", "glorious",
                                "so glorious", "very glorious", "adorable",
                                "excellent", "amazing"],
                               [".", "..", "...", "!", "!!", "!!!"]],
                 comments_per_day=0,
                 tag_list=['cat', 'car', 'dog'],
                 max_like_for_one_tag=5,
                 unfollow_break_min=15,
                 unfollow_break_max=30,
                 log_mod=0,
                 proxy="",
                 user_blacklist={},
                 tag_blacklist=[],
                 unwanted_username_list=[],
                 unfollow_whitelist=[]):

        self.database_name = database_name
        self.follows_db = sqlite3.connect(database_name, timeout=0, isolation_level=None)
        self.follows_db_c = self.follows_db.cursor()
        check_and_update(self)
        fake_ua = UserAgent()
        self.user_agent = check_and_insert_user_agent(self, str(fake_ua.random))
        self.bot_start = datetime.datetime.now()
        self.start_at_h = start_at_h
        self.start_at_m = start_at_m
        self.end_at_h = end_at_h
        self.end_at_m = end_at_m
        self.unfollow_break_min = unfollow_break_min
        self.unfollow_break_max = unfollow_break_max
        self.user_blacklist = user_blacklist
        self.tag_blacklist = tag_blacklist
        self.unfollow_whitelist = unfollow_whitelist
        self.comment_list = comment_list

        self.time_in_day = 24 * 60 * 60
        # Like
        self.like_per_day = like_per_day
        if self.like_per_day != 0:
            self.like_delay = self.time_in_day / self.like_per_day

        # Follow
        self.follow_time = follow_time
        self.follow_per_day = follow_per_day
        if self.follow_per_day != 0:
            self.follow_delay = self.time_in_day / self.follow_per_day

        # Unfollow
        self.unfollow_per_day = unfollow_per_day
        if self.unfollow_per_day != 0:
            self.unfollow_delay = self.time_in_day / self.unfollow_per_day

        # Comment
        self.comments_per_day = comments_per_day
        if self.comments_per_day != 0:
            self.comments_delay = self.time_in_day / self.comments_per_day

        # Don't like if media have more than n likes.
        self.media_max_like = media_max_like
        # Don't like if media have less than n likes.
        self.media_min_like = media_min_like
        # Auto mod seting:
        # Default list of tag.
        self.tag_list = tag_list
        # Get random tag, from tag_list, and like (1 to n) times.
        self.max_like_for_one_tag = max_like_for_one_tag
        # log_mod 0 to console, 1 to file
        self.log_mod = log_mod
        self.s = requests.Session()
        # if you need proxy make something like this:
        # self.s.proxies = {"https" : "http://proxyip:proxyport"}
        # by @ageorgios
        if proxy != "":
            proxies = {
                'http': 'http://' + proxy,
                'https': 'http://' + proxy,
            }
            self.s.proxies.update(proxies)
        # convert login to lower
        self.user_login = login.lower()
        self.user_password = password
        self.bot_mode = 0
        self.media_by_tag = []
        self.media_on_feed = []
        self.media_by_user = []
        self.unwanted_username_list = unwanted_username_list
        now_time = datetime.datetime.now()
        log_string = 'Instabot v1.2.0 started at %s:\n' % \
                     (now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        self.login()
        self.populate_user_blacklist()
        signal.signal(signal.SIGTERM, self.cleanup)
        atexit.register(self.cleanup)

    def populate_user_blacklist(self):
        for user in self.user_blacklist:
            user_id_url = self.url_user_detail % (user)
            info = self.s.get(user_id_url)

            # prevent error if 'Account of user was deleted or link is invalid
            from json import JSONDecodeError
            try:
                all_data = json.loads(info.text)
            except JSONDecodeError as e:
                self.write_log('Account of user %s was deleted or link is '
                               'invalid' % (user))
            else:
                # prevent exception if user have no media
                id_user = all_data['user']['id']
                # Update the user_name with the user_id
                self.user_blacklist[user] = id_user
                log_string = "Blacklisted user %s added with ID: %s" % (user,
                                                                        id_user)
                self.write_log(log_string)
                time.sleep(5 * random.random())

    def login(self):
        log_string = 'Trying to login as %s...\n' % (self.user_login)
        self.write_log(log_string)
        self.login_post = {
            'username': self.user_login,
            'password': self.user_password
        }

        self.s.headers.update({
            'Accept': '*/*',
            'Accept-Language': self.accept_language,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })

        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.s.post(
            self.url_login, data=self.login_post, allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        #ig_vw=1536; ig_pr=1.25; ig_vh=772;  ig_or=landscape-primary;
        self.s.cookies['ig_vw'] = '1536'
        self.s.cookies['ig_pr'] = '1.25'
        self.s.cookies['ig_vh'] = '772'
        self.s.cookies['ig_or'] = 'landscape-primary'
        time.sleep(5 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                ui = UserInfo()
                self.user_id = ui.get_user_id_by_login(self.user_login)
                self.login_status = True
                log_string = '%s login success!' % (self.user_login)
                self.write_log(log_string)
            else:
                self.login_status = False
                self.write_log('Login error! Check your login data!')
        else:
            self.write_log('Login error! Connection error!')

    def logout(self):
        now_time = datetime.datetime.now()
        log_string = 'Logout: likes - %i, follow - %i, unfollow - %i, comments - %i.' % \
                     (self.like_counter, self.follow_counter,
                      self.unfollow_counter, self.comments_counter)
        self.write_log(log_string)
        work_time = datetime.datetime.now() - self.bot_start
        log_string = 'Bot work time: %s' % (work_time)
        self.write_log(log_string)

        try:
            logout_post = {'csrfmiddlewaretoken': self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            self.write_log("Logout success!")
            self.login_status = False
        except:
            logging.exception("Logout error!")

    def cleanup(self, *_):
        # Unfollow all bot follow
        if self.follow_counter >= self.unfollow_counter:
            for f in self.bot_follow_list:
                log_string = "Trying to unfollow: %s" % (f[0])
                self.write_log(log_string)
                self.unfollow_on_cleanup(f[0])
                sleeptime = random.randint(self.unfollow_break_min,
                                           self.unfollow_break_max)
                log_string = "Pausing for %i seconds... %i of %i" % (
                    sleeptime, self.unfollow_counter, self.follow_counter)
                self.write_log(log_string)
                time.sleep(sleeptime)
                self.bot_follow_list.remove(f)

        # Logout
        if self.login_status:
            self.logout()

    def get_media_id_by_tag(self, tag):
        """ Get media ID set, by your hashtag """

        if self.login_status:
            log_string = "Get media id by tag: %s" % (tag)
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = self.url_tag % (tag)
                try:
                    r = self.s.get(url_tag)
                    all_data = json.loads(r.text)
                    self.media_by_tag = list(all_data['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
                except:
                    self.media_by_tag = []
                    self.write_log("Except on get_media!")
                    logging.exception("get_media_id_by_tag")
            else:
                return 0

    def get_instagram_url_from_media_id(self, media_id, url_flag=True, only_code=None):
        """ Get Media Code or Full Url from Media ID Thanks to Nikished """
        media_id = int(media_id)
        if url_flag is False: return ""
        else:
            alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
            shortened_id = ''
            while media_id > 0:
                media_id, idx = divmod(media_id, 64)
                shortened_id = alphabet[idx] + shortened_id
            if only_code: return shortened_id
            else: return 'instagram.com/p/' + shortened_id + '/'

    def get_username_by_media_id(self, media_id):
        """ Get username by media ID Thanks to Nikished """

        if self.login_status:
            if self.login_status == 1:
                media_id_url = self.get_instagram_url_from_media_id(int(media_id), only_code=True)
                url_media = self.url_media_detail % (media_id_url)
                try:
                    r = self.s.get(url_media)
                    all_data = json.loads(r.text)

                    username = str(all_data['graphql']['shortcode_media']['owner']['username'])
                    self.write_log("media_id=" + media_id + ", media_id_url=" +
                                   media_id_url + ", username_by_media_id=" + username)
                    return username
                except:
                    logging.exception("username_by_mediaid exception")
                    return False
            else:
                return ""

    def get_username_by_user_id(self, user_id):
        """ Get username by user_id """
        if self.login_status:
            try:
                url_info = self.api_user_detail % user_id
                r = self.s.get(url_info, headers="")
                all_data = json.loads(r.text)
                username = all_data["user"]["username"]
                return username
            except:
                logging.exception("Except on get_username_by_user_id")
                return False
        else:
            return False

    def get_userinfo_by_name(self, username):
        """ Get user info by name """

        if self.login_status:
            if self.login_status == 1:
                url_info = self.url_user_detail % (username)
                try:
                    r = self.s.get(url_info)
                    all_data = json.loads(r.text)
                    user_info = all_data['user']
                    follows = user_info['follows']['count']
                    follower = user_info['followed_by']['count']
                    follow_viewer = user_info['follows_viewer']
                    if follower > 3000 or follows > 1500:
                        self.write_log('   >>>This is probably Selebgram, Business or Fake account')
                    if follow_viewer:
                        return None
                    return user_info
                except:
                    logging.exception("Except on get_userinfo_by_name")
                    return False
            else:
                return False

    def like_all_exist_media(self, media_size=-1, delay=True):
        """ Like all media ID that have self.media_by_tag """

        if self.login_status:
            if self.media_by_tag != 0:
                i = 0
                for d in self.media_by_tag:
                    # Media count by this tag.
                    if media_size > 0 or media_size < 0:
                        media_size -= 1
                        l_c = self.media_by_tag[i]['node']['edge_liked_by']['count']
                        if ((l_c <= self.media_max_like and
                             l_c >= self.media_min_like) or
                            (self.media_max_like == 0 and
                             l_c >= self.media_min_like) or
                            (self.media_min_like == 0 and
                             l_c <= self.media_max_like) or
                            (self.media_min_like == 0 and
                             self.media_max_like == 0)):
                            for blacklisted_user_name, blacklisted_user_id in self.user_blacklist.items(
                            ):
                                if self.media_by_tag[i]['node']['owner'][
                                        'id'] == blacklisted_user_id:
                                    self.write_log(
                                        "Not liking media owned by blacklisted user: "
                                        + blacklisted_user_name)
                                    return False
                            if self.media_by_tag[i]['node']['owner'][
                                    'id'] == self.user_id:
                                self.write_log(
                                    "Keep calm - It's your own media ;)")
                                return False
                            if check_already_liked(self, media_id=self.media_by_tag[i]['node']['id']) == 1:
                                self.write_log("Keep calm - It's already liked ;)")
                                return False
                            try:
                                if (len(self.media_by_tag[i]['node']['edge_media_to_caption']['edges']) > 1):
                                    caption = self.media_by_tag[i]['node']['edge_media_to_caption'][
                                        'edges'][0]['node']['text'].encode(
                                            'ascii', errors='ignore')
                                    tag_blacklist = set(self.tag_blacklist)
                                    if sys.version_info[0] == 3:
                                        tags = {
                                            str.lower(
                                                (tag.decode('ASCII')).strip('#'))
                                            for tag in caption.split()
                                            if (tag.decode('ASCII')
                                                ).startswith("#")
                                        }
                                    else:
                                        tags = {
                                            unicode.lower(
                                                (tag.decode('ASCII')).strip('#'))
                                            for tag in caption.split()
                                            if (tag.decode('ASCII')
                                                ).startswith("#")
                                        }

                                    if tags.intersection(tag_blacklist):
                                        matching_tags = ', '.join(
                                            tags.intersection(tag_blacklist))
                                        self.write_log(
                                            "Not liking media with blacklisted tag(s): "
                                            + matching_tags)
                                        return False
                            except:
                                logging.exception("Except on like_all_exist_media")
                                return False

                            log_string = "Trying to like media: %s" % \
                                         (self.media_by_tag[i]['node']['id'])
                            self.write_log(log_string)
                            like = self.like(self.media_by_tag[i]['node']['id'])
                            # comment = self.comment(self.media_by_tag[i]['id'], 'Cool!')
                            # follow = self.follow(self.media_by_tag[i]["owner"]["id"])
                            if like != 0:
                                if like.status_code == 200:
                                    # Like, all ok!
                                    self.error_400 = 0
                                    self.like_counter += 1
                                    log_string = "Liked: %s. Like #%i." % \
                                                 (self.media_by_tag[i]['node']['id'],
                                                  self.like_counter)
                                    insert_media(self,
                                                 media_id=self.media_by_tag[i]['node']['id'],
                                                 status="200")
                                    self.write_log(log_string)
                                elif like.status_code == 400:
                                    log_string = "Not liked: %i" \
                                                 % (like.status_code)
                                    self.write_log(log_string)
                                    insert_media(self,
                                                 media_id=self.media_by_tag[i]['node']['id'],
                                                 status="400")
                                    # Some error. If repeated - can be ban!
                                    if self.error_400 >= self.error_400_to_ban:
                                        # Look like you banned!
                                        time.sleep(self.ban_sleep_time)
                                    else:
                                        self.error_400 += 1
                                else:
                                    log_string = "Not liked: %i" \
                                                 % (like.status_code)
                                    insert_media(self,
                                                 media_id=self.media_by_tag[i]['node']['id'],
                                                 status=str(like.status_code))
                                    self.write_log(log_string)
                                    return False
                                    # Some error.
                                i += 1
                                if delay:
                                    time.sleep(self.like_delay * 0.9 +
                                               self.like_delay * 0.2 *
                                               random.random())
                                else:
                                    return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
            else:
                self.write_log("No media to like!")

    def like(self, media_id):
        """ Send http request to like media by ID """
        if self.login_status:
            url_likes = self.url_likes % (media_id)
            try:
                like = self.s.post(url_likes)
                last_liked_media_id = media_id
            except:
                logging.exception("Except on like!")
                like = 0
            return like

    def unlike(self, media_id):
        """ Send http request to unlike media by ID """
        if self.login_status:
            url_unlike = self.url_unlike % (media_id)
            try:
                unlike = self.s.post(url_unlike)
            except:
                logging.exception("Except on unlike!")
                unlike = 0
            return unlike

    def comment(self, media_id, comment_text):
        """ Send http request to comment """
        if self.login_status:
            comment_post = {'comment_text': comment_text}
            url_comment = self.url_comment % (media_id)
            try:
                comment = self.s.post(url_comment, data=comment_post)
                if comment.status_code == 200:
                    self.comments_counter += 1
                    log_string = 'Write: "%s". #%i.' % (comment_text,
                                                        self.comments_counter)
                    self.write_log(log_string)
                return comment
            except:
                logging.exception("Except on comment!")
        return False

    def follow(self, user_id):
        """ Send http request to follow """
        if self.login_status:
            url_follow = self.url_follow % (user_id)
            try:
                follow = self.s.post(url_follow)
                if follow.status_code == 200:
                    self.follow_counter += 1
                    log_string = "Followed: %s #%i." % (user_id,
                                                        self.follow_counter)
                    self.write_log(log_string)
                    username = self.get_username_by_user_id(user_id=user_id)
                    insert_username(self, user_id=user_id, username=username)
                return follow
            except:
                logging.exception("Except on follow!")
        return False

    def unfollow(self, user_id):
        """ Send http request to unfollow """
        if self.login_status:
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    log_string = "Unfollowed: %s #%i." % (user_id,
                                                          self.unfollow_counter)
                    self.write_log(log_string)
                return unfollow
            except:
                logging.exception("Exept on unfollow!")
        return False

    def unfollow_on_cleanup(self, user_id):
        """ Unfollow on cleanup by @rjmayott """
        if self.login_status:
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    log_string = "Unfollow: %s #%i of %i." % (
                        user_id, self.unfollow_counter, self.follow_counter)
                    self.write_log(log_string)
                else:
                    log_string = "Slow Down - Pausing for 5 minutes so we don't get banned!"
                    self.write_log(log_string)
                    time.sleep(300)
                    unfollow = self.s.post(url_unfollow)
                    if unfollow.status_code == 200:
                        self.unfollow_counter += 1
                        log_string = "Unfollow: %s #%i of %i." % (
                            user_id, self.unfollow_counter,
                            self.follow_counter)
                        self.write_log(log_string)
                    else:
                        log_string = "Still no good :( Skipping and pausing for another 5 minutes"
                        self.write_log(log_string)
                        time.sleep(300)
                    return False
                return unfollow
            except:
                log_string = "Except on unfollow... Looks like a network error"
                logging.exception(log_string)
        return False

    def auto_mod(self):
        """ Star loop, that get media ID by your tag list, and like it """
        if self.login_status:
            while True:
                random.shuffle(self.tag_list)
                self.get_media_id_by_tag(random.choice(self.tag_list))
                self.like_all_exist_media(random.randint \
                                              (1, self.max_like_for_one_tag))

    def new_auto_mod(self):
        while True:
            now = datetime.datetime.now()
            if (
                    datetime.time(self.start_at_h, self.start_at_m) <= now.time()
                    and now.time() <= datetime.time(self.end_at_h, self.end_at_m)
            ):
                # ------------------- Get media_id -------------------
                if len(self.media_by_tag) == 0:
                    self.get_media_id_by_tag(random.choice(self.tag_list))
                    self.this_tag_like_count = 0
                    self.max_tag_like_count = random.randint(
                        1, self.max_like_for_one_tag)
                    self.remove_already_liked()
                # ------------------- Like -------------------
                self.new_auto_mod_like()
                # ------------------- Follow -------------------
                self.new_auto_mod_follow()
                # ------------------- Unfollow -------------------
                self.new_auto_mod_unfollow()
                # ------------------- Comment -------------------
                self.new_auto_mod_comments()
                # Bot iteration in 1 sec
                time.sleep(3)
                # print("Tic!")
            else:
                print("sleeping until {hour}:{min}".format(hour=self.start_at_h,
                                                           min=self.start_at_m), end="\r")
                time.sleep(100)

    def remove_already_liked(self):
        self.write_log("Removing already liked medias..")
        x = 0
        while x < len(self.media_by_tag):
            if check_already_liked(self, media_id=self.media_by_tag[x]['node']['id']) == 1:
                self.media_by_tag.remove(self.media_by_tag[x])
            else:
                x += 1

    def new_auto_mod_like(self):
        if time.time() > self.next_iteration["Like"] and self.like_per_day != 0 \
                and len(self.media_by_tag) > 0:
            # You have media_id to like:
            if self.like_all_exist_media(media_size=1, delay=False):
                # If like go to sleep:
                self.next_iteration["Like"] = time.time() + \
                                              self.add_time(self.like_delay)
                # Count this tag likes:
                self.this_tag_like_count += 1
                if self.this_tag_like_count >= self.max_tag_like_count:
                    self.media_by_tag = [0]
            # Del first media_id
            del self.media_by_tag[0]

    def new_auto_mod_follow(self):
        if time.time() > self.next_iteration["Follow"] and \
                        self.follow_per_day != 0 and len(self.media_by_tag) > 0:
            if self.media_by_tag[0]['node']["owner"]["id"] == self.user_id:
                self.write_log("Keep calm - It's your own profile ;)")
                return
            if check_already_followed(self, user_id=self.media_by_tag[0]['node']["owner"]["id"]) == 1:
                self.write_log("Already followed before " + self.media_by_tag[0]['node']["owner"]["id"])
                self.next_iteration["Follow"] = time.time() + \
                                                self.add_time(self.follow_delay/2)
                return
            log_string = "Trying to follow: %s" % (
                self.media_by_tag[0]['node']["owner"]["id"])
            self.write_log(log_string)

            if self.follow(self.media_by_tag[0]['node']["owner"]["id"]) != False:
                self.bot_follow_list.append(
                    [self.media_by_tag[0]['node']["owner"]["id"], time.time()])
                self.next_iteration["Follow"] = time.time() + \
                                                self.add_time(self.follow_delay)

    def new_auto_mod_unfollow(self):
        if time.time() > self.next_iteration["Unfollow"] and self.unfollow_per_day != 0:
            if self.bot_mode == 0:
                log_string = "Trying to unfollow #%i: " % (self.unfollow_counter + 1)
                self.write_log(log_string)
                self.auto_unfollow()
                self.next_iteration["Unfollow"] = time.time() + \
                                                    self.add_time(self.unfollow_delay)
            if self.bot_mode == 1:
                unfollow_protocol(self)

    def new_auto_mod_comments(self):
        if time.time() > self.next_iteration["Comments"] and self.comments_per_day != 0 \
                and len(self.media_by_tag) > 0 \
                and self.check_exisiting_comment(self.media_by_tag[0]['node']['shortcode']) == False:
            comment_text = self.generate_comment()
            log_string = "Trying to comment: %s" % (self.media_by_tag[0]['node']['id'])
            self.write_log(log_string)
            if self.comment(self.media_by_tag[0]['node']['id'], comment_text) != False:
                self.next_iteration["Comments"] = time.time() + \
                                                  self.add_time(self.comments_delay)

    def add_time(self, time):
        """ Make some random for next iteration"""
        return time * 0.9 + time * 0.2 * random.random()

    def generate_comment(self):
        c_list = list(itertools.product(*self.comment_list))

        repl = [("  ", " "), (" .", "."), (" !", "!")]
        res = " ".join(random.choice(c_list))
        for s, r in repl:
            res = res.replace(s, r)
        return res.capitalize()

    def check_exisiting_comment(self, media_code):
        url_check = self.url_media_detail % (media_code)
        check_comment = self.s.get(url_check)
        if check_comment.status_code == 200:
            all_data = json.loads(check_comment.text)
            if all_data['graphql']['shortcode_media']['owner']['id'] == self.user_id:
                self.write_log("Keep calm - It's your own media ;)")
                # Del media to don't loop on it
                del self.media_by_tag[0]
                return True
            comment_list = list(all_data['graphql']['shortcode_media']['edge_media_to_comment']['edges'])
            for d in comment_list:
                if d['node']['owner']['id'] == self.user_id:
                    self.write_log("Keep calm - Media already commented ;)")
                    # Del media to don't loop on it
                    del self.media_by_tag[0]
                    return True
            return False
        else:
            insert_media(self, self.media_by_tag[0]['node']['id'], str(check_comment.status_code))
            self.media_by_tag.remove(self.media_by_tag[0])
            return False

    def auto_unfollow(self):
        checking = True
        while checking:
            username_row = get_username_random(self)
            if not username_row:
                self.write_log("Looks like there is nobody to unfollow.")
                return False
            current_id = username_row[0]
            current_user = username_row[1]
            unfollow_count = username_row[2]

            if not current_user:
                current_user = self.get_username_by_user_id(user_id=current_id)
            if not current_user:
                log_string = "api limit reached from instagram. Will try later"
                self.write_log(log_string)
                return False
            for wluser in self.unfollow_whitelist:
                if wluser == current_user:
                    log_string = (
                        "found whitelist user, starting search again")
                    self.write_log(log_string)
                    break
            else:
                checking = False

        if self.login_status:
            log_string = "Getting user info : %s" % current_user
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = self.url_user_detail % (current_user)
                try:
                    r = self.s.get(url_tag)
                    all_data = json.loads(r.text)

                    user_info = all_data['user']
                    i = 0
                    log_string = "Checking user info.."
                    self.write_log(log_string)

                    follows = user_info['follows']['count']
                    follower = user_info['followed_by']['count']
                    media = user_info['media']['count']
                    follow_viewer = user_info['follows_viewer']
                    followed_by_viewer = user_info[
                        'followed_by_viewer']
                    requested_by_viewer = user_info[
                        'requested_by_viewer']
                    has_requested_viewer = user_info[
                        'has_requested_viewer']
                    log_string = "Follower : %i" % (follower)
                    self.write_log(log_string)
                    log_string = "Following : %s" % (follows)
                    self.write_log(log_string)
                    log_string = "Media : %i" % (media)
                    self.write_log(log_string)
                    if follows == 0 or follower / follows > 2:
                        self.is_selebgram = True
                        self.is_fake_account = False
                        print('   >>>This is probably Selebgram account')
                    elif follower == 0 or follows / follower > 2:
                        self.is_fake_account = True
                        self.is_selebgram = False
                        print('   >>>This is probably Fake account')
                    else:
                        self.is_selebgram = False
                        self.is_fake_account = False
                        print('   >>>This is a normal account')

                    if media > 0 and follows / media < 25 and follower / media < 25:
                        self.is_active_user = True
                        print('   >>>This user is active')
                    else:
                        self.is_active_user = False
                        print('   >>>This user is passive')

                    if follow_viewer or has_requested_viewer:
                        self.is_follower = True
                        print("   >>>This account is following you")
                    else:
                        self.is_follower = False
                        print('   >>>This account is NOT following you')

                    if followed_by_viewer or requested_by_viewer:
                        self.is_following = True
                        print('   >>>You are following this account')

                    else:
                        self.is_following = False
                        print('   >>>You are NOT following this account')

                except:
                    logging.exception("Except on auto_unfollow!")
                    time.sleep(3)
                    return False
            else:
                return False

            if (
                    self.is_selebgram is not False
                    or self.is_fake_account is not False
                    or self.is_active_user is not True
                    or self.is_follower is not True
            ):
                self.write_log(current_user)
                self.unfollow(current_id)
                insert_unfollow_count(self, user_id=current_id)

    def get_media_id_recent_feed(self):
        if self.login_status:
            now_time = datetime.datetime.now()
            log_string = "%s : Get media id on recent feed" % (self.user_login)
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = 'https://www.instagram.com/?__a=1'
                try:
                    r = self.s.get(url_tag)
                    all_data = json.loads(r.text)

                    self.media_on_feed = list(
                        all_data['graphql']['user']['edge_web_feed_timeline'][
                            'edges'])

                    log_string = "Media in recent feed = %i" % (
                        len(self.media_on_feed))
                    self.write_log(log_string)
                except:
                    logging.exception("get_media_id_recent_feed")
                    self.media_on_feed = []
                    time.sleep(20)
                    return 0
            else:
                return 0

    def write_log(self, log_text):
        """ Write log by print() or logger """

        if self.log_mod == 0:
            try:
                now_time = datetime.datetime.now()
                print(now_time.strftime("%d.%m.%Y_%H:%M")  + " " + log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")
        elif self.log_mod == 1:
            # Create log_file if not exist.
            if self.log_file == 0:
                self.log_file = 1
                now_time = datetime.datetime.now()
                self.log_full_path = '%s%s_%s.log' % (
                    self.log_file_path, self.user_login,
                    now_time.strftime("%d.%m.%Y_%H:%M"))
                formatter = logging.Formatter('%(asctime)s - %(name)s '
                                              '- %(message)s')
                self.logger = logging.getLogger(self.user_login)
                self.hdrl = logging.FileHandler(self.log_full_path, mode='w')
                self.hdrl.setFormatter(formatter)
                self.logger.setLevel(level=logging.INFO)
                self.logger.addHandler(self.hdrl)
            # Log to log file.
            try:
                self.logger.info(log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")
