#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import requests
import random
import time
import datetime
import logging
import json
import atexit
import signal
import itertools

class InstaBot:
    """
    Instagram bot v 1.0
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

    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    # If instagram ban you - query return 400 error.
    error_400 = 0
    # If you have 3 400 error in row - looks like you banned.
    error_400_to_ban = 3
    # If InstaBot think you are banned - going to sleep.
    ban_sleep_time = 2*60*60

    # All counter.
    like_counter = 0
    follow_counter = 0
    unfollow_counter = 0
    comments_counter = 0
    current_user ='hajka'
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
    is_fake_account  = False
    is_active_user = False
    is_following = False
    is_follower = False
    is_rejected = False
    is_self_checking = False
    is_by_tag = False
    is_follower_number = 0

    self_following = 0
    self_follower = 0
    log_file_path = '/mnt/sdcard0/daemonx/log/'
    log_file = 0

    # Other.
    media_by_tag = 0
    media_by_user = []
    login_status = False
    # For new_auto_mod
    next_iteration = {"Like": 0, "Follow": 0, "Unfollow": 0, "Comments": 0}

    def __init__(self, login, password,
                like_per_day=1000,
                media_max_like=20000,
                media_min_like=0,
                follow_per_day=0,
                follow_time=5*60*60,
                unfollow_per_day=0,
                comments_per_day=0,
                tag_list=['cat', 'car', 'dog'],
                max_like_for_one_tag = 5,
                unfollow_break_min=150,
                unfollow_break_max=300,
                log_mod = 0):
        self.bot_start = datetime.datetime.now()
        self.unfollow_break_min = unfollow_break_min
        self.unfollow_break_max = unfollow_break_max
        self.time_in_day = 12*60*60
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
        # self.s.proxies = {"https" : "http://proxyip:proxyport"
        # by @ageorgios

        # convert login to lower
        self.user_login = login.lower()
        self.user_password = password
        self.media_by_tag = []
        self.ex_user_list = []
        self.unwanted_username_list = ['second','stuff','art','project','love','life','food','blog','free','keren','photo','graphy','indo','travel','art','shop','store','sex','toko','jual','online','murah','jam','kaos','case','baju','fashion',
                                        'corp','tas','butik','grosir','karpet','sosis','salon','skin','care','cloth','tech','rental',
                                        'kamera','beauty','express','kredit','collection','impor','preloved','follow','follower','gain',
                                        '.id','_id','bags']

        now_time = datetime.datetime.now()
        log_string = 'Instabot v1.0.1 started at %s:\n' %\
                     (now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        self.login()

        signal.signal(signal.SIGTERM, self.cleanup)
        atexit.register(self.cleanup)
        

    def login(self):
        log_string = 'Trying to login as %s...\n' % (self.user_login)
        self.write_log(log_string)
        self.s.cookies.update ({'sessionid' : '', 'mid' : '', 'ig_pr' : '1',
                               'ig_vw' : '1920', 'csrftoken' : '',
                               's_network' : '', 'ds_user_id' : ''})
        self.login_post = {'username' : self.user_login,
                           'password' : self.user_password}
        self.s.headers.update ({'Accept-Encoding' : 'gzip, deflate',
                               'Accept-Language' : self.accept_language,
                               'Connection' : 'keep-alive',
                               'Content-Length' : '0',
                               'Host' : 'www.instagram.com',
                               'Origin' : 'https://www.instagram.com',
                               'Referer' : 'https://www.instagram.com/',
                               'User-Agent' : self.user_agent,
                               'X-Instagram-AJAX' : '1',
                               'X-Requested-With' : 'XMLHttpRequest'})
        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken' : r.cookies['csrftoken']})
        time.sleep(1 * random.random())
        login = self.s.post(self.url_login, data=self.login_post,
                            allow_redirects=True)
        self.s.headers.update({'X-CSRFToken' : login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(1 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
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
        log_string = 'Logout: likes - %i, follow - %i, unfollow - %i, comments - %i.' %\
                     (self.like_counter, self.follow_counter,
                      self.unfollow_counter, self.comments_counter)
        self.write_log(log_string)
        work_time = datetime.datetime.now() - self.bot_start
        log_string = 'Bot work time: %s' %(work_time)
        self.write_log(log_string)

        try:
            logout_post = {'csrfmiddlewaretoken' : self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            self.write_log("Logout success!")
            self.login_status = False
        except:
            self.write_log("Logout error!")

    def cleanup (self, *_):
        # Unfollow all bot follow
        if self.follow_counter >= self.unfollow_counter:
            for f in self.bot_follow_list:
                log_string = "Trying to unfollow: %s" % (f[0])
                self.write_log(log_string)
                self.unfollow_on_cleanup(f[0])
                sleeptime = random.randint(self.unfollow_break_min, self.unfollow_break_max)
                log_string = "Pausing for %i seconds... %i of %i" % (sleeptime, self.unfollow_counter, self.follow_counter)
                self.write_log(log_string)
                time.sleep(sleeptime)
                self.bot_follow_list.remove(f)

        # Logout
        if (self.login_status):
            self.logout()
        exit(0)

 
    def like(self, media_id):
        """ Send http request to like media by ID """
        if (self.login_status):
            url_likes = self.url_likes % (media_id)
            try:
                like = self.s.post(url_likes)
                last_liked_media_id = media_id
            except:
                self.write_log("Except on like!")
                like = 0
                del self.media_by_user[self.current_index]
            return like

    def unlike(self, media_id):
        """ Send http request to unlike media by ID """
        if (self.login_status):
            url_unlike = self.url_unlike % (media_id)
            try:
                unlike = self.s.post(url_unlike)
            except:
                self.write_log("Except on unlike!")
                unlike = 0
            return unlike

    def comment(self, media_id, comment_text):
        """ Send http request to comment """
        if (self.login_status):
            comment_post = {'comment_text' : comment_text}
            url_comment = self.url_comment % (media_id)
            try:
                comment = self.s.post(url_comment, data=comment_post)
                if comment.status_code == 200:
                    self.comments_counter += 1
                    log_string = 'Write: "%s". #%i.' % (comment_text, self.comments_counter)
                    self.write_log(log_string)
                return comment
            except:
                self.write_log("Except on comment!")
        return False

    def follow(self, user_id):
        """ Send http request to follow """
        if (self.login_status):
            url_follow = self.url_follow % (user_id)
            try:
                follow = self.s.post(url_follow)
                if follow.status_code == 200:
                    self.follow_counter += 1
                    log_string = "Followed: %s #%i." % (user_id, self.follow_counter)
                    self.write_log(log_string)
                return follow
            except:
                self.write_log("Except on follow!")
        return False

    def like_all_exist_media (self, media_size=-1, delay=True):
        """ Like all media ID that have self.media_by_tag """

        if (self.login_status):
            if self.media_by_user != 0:
                i=self.current_index
                for d in self.media_by_user:
                    # Media count by this user.
                    if media_size > 0 or media_size < 0:
                        media_size -= 1
                        l_c = self.media_by_user[i]['likes']['count']
                        if l_c < 50:
                            log_string = "Trying to like media: %s" %\
                                         (self.media_by_user[i]['id'])
                            self.write_log(log_string)
                            like = self.like(self.media_by_user[i]['id'])
                            # comment = self.comment(self.media_by_tag[i]['id'], 'Cool!')
                            # follow = self.follow(self.media_by_tag[i]["owner"]["id"])
                            if like != 0:
                                if like.status_code == 200:
                                    # Like, all ok!
                                    self.error_400 = 0
                                    self.like_counter += 1
                                    log_string = "Liked: %s. Likes: #%i." %\
                                                 (self.media_by_user[i]['id'],
                                                  self.media_by_user[i]['likes']['count'])
                                    self.write_log(log_string)
                                elif like.status_code == 400:
                                    log_string = "Not liked: %i" \
                                                  % (like.status_code)
                                    self.write_log(log_string)
                                    # Some error. If repeated - can be ban!
                                    if self.error_400 >= self.error_400_to_ban:
                                        # Look like you banned!
                                        time.sleep(self.ban_sleep_time)
                                    else:
                                        self.error_400 += 1
                                else:
                                    log_string = "Not liked: %i" \
                                                  % (like.status_code)
                                    self.write_log(log_string)
                                    return False
                                    # Some error
                                if delay:
                                    time.sleep(self.like_delay*0.9 +
                                           self.like_delay*0.2*random.random())
                                else:
                                    return True
                            else:
                                return False
                        else:
                            print('Too much liker for this media!!! LC = %i' % (l_c))
                            return True
                    else:
                        return False
            else:
                self.write_log("No media to like!")


    def unfollow(self, user_id, user_name):
        """ Send http request to unfollow """
        if (self.login_status):
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    log_string = "Unfollow: %s #%i." % (user_name, self.unfollow_counter)
                    self.write_log(log_string)
                return unfollow
            except:
                self.write_log("Exept on unfollow!")
        return False

    def unfollow_on_cleanup(self, user_id):
        """ Unfollow on cleanup by @rjmayott """
        if (self.login_status):
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    log_string = "Unfollow: %s #%i of %i." % (user_id, self.unfollow_counter, self.follow_counter)
                    self.write_log(log_string)
                else:
                    log_string = "Slow Down - Pausing for 5 minutes so we don't get banned!"
                    self.write_log(log_string)
                    time.sleep(300)
                    unfollow = self.s.post(url_unfollow)
                    if unfollow.status_code == 200:
                        self.unfollow_counter += 1
                        log_string = "Unfollow: %s #%i of %i." % (user_id, self.unfollow_counter, self.follow_counter)
                        self.write_log(log_string)
                    else:
                        log_string = "Still no good :( Skipping and pausing for another 5 minutes"
                        self.write_log(log_string)
                        time.sleep(300)
                    return False
                return unfollow
            except:
                log_string = "Except on unfollow... Looks like a network error"
                self.write_log(log_string)
        return False

    def auto_mod(self):
        """ Star loop, that get media ID by your tag list, and like it """
        if (self.login_status):
            while True:
                random.shuffle(self.tag_list)
                self.get_media_id_by_tag(random.choice(self.tag_list))
                self.like_all_exist_media(random.randint \
                                         (1, self.max_like_for_one_tag))

    # Method to get media id on my recent feed
    def new_auto_mod(self):
        #To limit how many photos on recent feed to scan
        limit = random.randint(4,6)
        print(limit)
        counterz = 0
        self.is_checked = False
        self.is_rejected = False
        while counterz<=limit:
            # ------------------- Get media_id -------------------
            if len(self.media_by_user) is 0:
                self.get_media_id_user_feed()
            # ------------------- Like -------------------
            if self.is_rejected is not False :
                return 0
            if self.is_follower is not False :
                print("@@@@@@@@@@@@@@ This is your follower B****h!!! @@@@@@@@@@@@@")
                self.is_follower_number += 1
                print ("%i") %(self.is_follower_number)
                return 
            self.new_auto_mod_like()
            counterz += 1
            # Bot iteration in 1 sec
            time.sleep(3*15)

    def new_auto_mod_like(self):
        if time.time()>self.next_iteration["Like"] and self.like_per_day!=0 \
            and len(self.media_by_user) > 0:
            # You have media_id to like:
                        self.current_index = random.randint(0,len(self.media_by_user)-1)
                        log_string = "Current Index = %i of %i medias"%(self.current_index, len(self.media_by_user))
                        self.write_log(log_string)
                        if self.like_all_exist_media(media_size=1, delay=False):
                # If like go to sleep:
                                self.next_iteration["Like"] = time.time() +\
                                              self.add_time(self.like_delay)
            # Del first media_id
                        del self.media_by_user[self.current_index]

    #Modified method...
    def new_auto_mod_unfollow2(self):

        log_string = "Trying to unfollow: %s" % (self.current_user)
        self.write_log(log_string)

        self.unfollow(self.current_id, self.current_user)
               
    def new_auto_mod_unfollow(self):
        if time.time()>self.next_iteration["Unfollow"] and \
            self.unfollow_per_day!=0 and len(self.bot_follow_list) > 0:
            for f in self.bot_follow_list:
                if time.time() > (f[1] + self.follow_time):

                    log_string = "Trying to unfollow #%i: %s" % (self.unfollow_counter, f[0])
                    self.write_log(log_string)

                    if self.unfollow(f[0]) != False:
                        self.bot_follow_list.remove(f)
                        self.next_iteration["Unfollow"] = time.time() +\
                                self.add_time(self.unfollow_delay)

    def new_auto_mod_comments(self):
        if time.time()>self.next_iteration["Comments"] and self.comments_per_day!=0 \
            and len(self.media_by_tag) > 0:

            comment_text = self.generate_comment()
            log_string = "Trying to comment: %s" % (self.media_by_tag[0]['id'])
            self.write_log(log_string)
            if self.comment(self.media_by_tag[0]['id'], comment_text) != False:
                self.next_iteration["Comments"] = time.time() +\
                                              self.add_time(self.comments_delay)

    def add_time(self, time):
        """ Make some random for next iteration"""
        return time*0.9 + time*0.2*random.random()

    def generate_comment(self):
        c_list = list(itertools.product(
                                                                ["woow..."],
                                    ["this", "the", "your"],
                                    ["photo", "picture", "pic", "shot", "snapshot"],
                                    ["is", "looks", "is really"],
                                    ["great", "super", "good", "very good",
                                    "good", "wow", "WOW", "cool",
                                    "GREAT", "magnificent", "magical", "very cool",
                                    "beautiful",
                                    "so beautiful",
                                    "lovely", "so lovely", "very lovely",
                                    "excellent", "amazing"],
                                    [".", "..", "...", "!", "!!", "!!!"]))

        repl = [("  ", " "), (" .", "."), (" !", "!")]
        res = " ".join(random.choice(c_list))
        for s, r in repl:
            res = res.replace(s, r)
        return res.capitalize()
        
    def new_auto_mod2(self):
        limit = random.randint(10,22)+1
        print(limit)

        while self.unfollow_counter<=limit:
            self.get_media_id_recent_feed()
            if len(self.media_by_tag) == 0:
                self.follow_counter=0
                self.new_auto_mod4()
            if len(self.media_by_tag) != 0 and self.is_follower_number < 5:
                chooser = random.randint(0,len(self.media_by_tag)-1)
                self.current_user=self.media_by_tag[chooser]["owner"]["username"]
                self.current_id=self.media_by_tag[chooser]["owner"]["id"]
                self.new_auto_mod()
                self.like_counter=0
                self.media_by_user = []
                if self.is_selebgram is not False or self.is_fake_account is not False or self.is_active_user is not True or self.is_follower is not True:
                    self.new_auto_mod_unfollow2()
                try:
                    del self.media_by_tag[chooser]
                except:
                    self.media_by_tag = []
            else :
                self.new_auto_mod4()
                self.is_follower_number = 0
            # Bot sleeping
            time.sleep(13+5)
            #print("Tac!")

    def new_auto_mod3(self):
        chooser = 0
        while len(self.user_list)>0 and chooser < len(self.user_list) :
            self.current_user=self.user_list[chooser]["user"]["username"]
            self.current_id=self.user_list[chooser]["user"]["id"]
            for index in range(len(self.unwanted_username_list)):
                if self.unwanted_username_list[index] in self.current_user :
                    print('Username = '+ self.current_user + '\n      ID = ' + self.current_id + '      <<< rejected ' + self.unwanted_username_list[index] +' is found!!!')
                    break
            else :
                for index in range(len(self.user_info_list)):
                    if self.current_user in self.user_info_list[index][0]:
                        print('Username = '+ self.current_user + '\n      ID = ' + self.current_id + '      <<< rejected this user is already in user info list!!!')
                        break
                else :
                    print('Username = '+ self.current_user + '\n      ID = ' + self.current_id + '      <<< added to user info list')
                    self.user_info_list.append([self.current_user,self.current_id])
            chooser += 1
        log_string="\nSize of user info list : %i Size of ex user list : %i \n" % (len(self.user_info_list), len(self.ex_user_list))
        self.write_log(log_string)
            
    def new_auto_mod4(self):
        limit = random.randint(5,10)+1
        print(limit)
        while self.follow_counter<limit:
            chooser = 0
            if len(self.user_info_list)>0:
                chooser = random.randint(0,len(self.user_info_list)-1)
                self.current_user=self.user_info_list[chooser][0]
                self.current_id=self.user_info_list[chooser][1]
                print('=============== \nCheck profile of '+self.current_user+'\n===============')
                self.get_user_info(self.current_user)
            else :
                print('xxxxxxx user info list is empty!!! xxxxxxxxx')
                self.new_auto_mod6()
            if self.is_selebgram!=True and self.is_fake_account!=True and self.is_active_user!=False :
                if self.is_following!=True :                
                    print('Trying to follow : ' + self.current_user + ' with user ID :' + self.current_id)
                    self.follow(self.current_id)
                    print('delete ' + self.user_info_list[chooser][0]+' from user info list')
                    del self.user_info_list[chooser]
            else :
                print('delete ' + self.user_info_list[chooser][0]+' from user info list')
                del self.user_info_list[chooser]
                
            # Bot iteration in 1 sec
            time.sleep(random.randint(13,26))
            #print("Tac!")

    def new_auto_mod5(self):
        limit = random.randint(1,3)
        counterx = 0
        print(limit)
        self.is_checked = False
        self.is_rejected = False
        while counterx<=limit:
        # ------------------- Get media_id -------------------
            if len(self.media_by_user) == 0:
                self.is_checked = False
                self.is_rejected = False
                self.get_media_id_user_feed()
        # ------------------- Like -------------------
            if self.is_rejected is not False :
                self.is_checked = False
                self.new_auto_mod_unfollow2()
                return 0
            self.new_auto_mod_like2()
            # Bot iteration in 1 sec
            time.sleep(random.randint(13,35))
            counterx += 1

    #Method to scan your recent feed and put some account to follow later into list
    def new_auto_mod6(self):
        #This is to limit how many people do you want to put into list before
        ##The bot start to check their profile one by one and start following them
        limit = random.randint(51,90)
        while len(self.user_info_list)<limit:
            #First the bot try to collect media id on your recent feed
            self.get_media_id_recent_feed()
            #If your account is old enough, there will be 24 photos on your recent feed
            if len(self.media_by_tag) > 23:
                print (self.is_follower_number)
                #Select the media on your recent feed randomly
                chooser = random.randint(0,len(self.media_by_tag)-1)
                #The bot will save the owner of the media name and use it to try checking his/her profile
                self.current_user=self.media_by_tag[chooser]["owner"]["username"]
                self.current_id=self.media_by_tag[chooser]["owner"]["id"]

            #If your account is new, and you don't following anyone, your recent feed will be empty   
            else:
                #If your recent feed is empty, then you start collecting media id by hashtag
                self.is_by_tag = True
                self.get_media_id_user_feed()
                max = 0
                while len(self.media_by_tag) > 5 and max < 5:
                    chooser = random.randint(0,len(self.media_by_tag)-1)
                    self.current_id=self.media_by_tag[chooser]["owner"]["id"]
                    self.follow(self.current_id)
                    del self.media_by_tag[chooser]
                    max += 1
                    time.sleep(30)
                self.is_by_tag = False
                self.media_by_tag = []
                continue
            if len(self.user_info_list)<10000:
                for index in range(len(self.ex_user_list)):
                    if self.ex_user_list[index][0] in self.current_user:
                        print('============================== \nUpss ' + self.current_user + ' is already in ex user list... \n==============================')
                        break
                else:
                    self.new_auto_mod5()
                    self.ex_user_list.append([self.current_user,self.current_id])
                self.user_list = []
                self.media_by_user = []
                self.media_by_tag = []
            else:
                break
            if len(self.ex_user_list)>20:
                chooser = random.randint(0,len(self.ex_user_list)-1)
                self.current_user=self.ex_user_list[chooser][0]
                self.current_id=self.ex_user_list[chooser][1]
                print('Trying to unfollow : ' + self.current_user)
                self.new_auto_mod_unfollow2()
                del self.ex_user_list[chooser]
            time.sleep(random.randint(15,22))
                         
            
    def new_auto_mod_like2(self):
        if time.time()>self.next_iteration["Like"] and self.like_per_day!=0 \
            and len(self.media_by_user) > 0:
            # You have media_id to like:
                        self.current_index = random.randint(0,len(self.media_by_user)-1)
                        log_string = "Current Index = %i of %i medias"%(self.current_index, len(self.media_by_user))
                        self.write_log(log_string)
                        #if self.like_all_exist_media(media_size=1, delay=False):
                # If like go to sleep:
                                #self.next_iteration["Like"] = time.time() +\
                                             #self.add_time(self.like_delay)
            # Del first media_id
                        if self.media_by_user[self.current_index]["likes"]["count"] >= 10 and self.media_by_user[self.current_index]["likes"]["count"] < 100:
                            self.get_user_id_post_page(self.media_by_user[self.current_index]["code"])
                            self.new_auto_mod3()
                        del self.media_by_user[self.current_index]

    def get_user_info (self, username):
        """ Get media ID set, by your hashtag """

        if (self.login_status):
            now_time = datetime.datetime.now()
            log_string = "%s : Get user info \n%s"%(self.user_login,now_time.strftime("%d.%m.%Y %H:%M"))
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = 'https://www.instagram.com/%s/'%(username)
                try:
                    r = self.s.get(url_tag)
                    text = r.text
                    finder_text_start = ('<script type="text/javascript">'
                                         'window._sharedData = ')
                    finder_text_start_len = len(finder_text_start)-1
                    finder_text_end = ';</script>'

                    all_data_start = text.find(finder_text_start)
                    all_data_end = text.find(finder_text_end, all_data_start + 1)
                    json_str = text[(all_data_start + finder_text_start_len + 1) \
                                   : all_data_end]
                    all_data = json.loads(json_str)
                                        
                    user_info = list(all_data['entry_data']['ProfilePage'])
                    i=0	
                    log_string="Checking user info.."
                    self.write_log(log_string)

                        
                    while i<1:
                        follows = user_info[0]['user']['follows']['count']
                        follower = user_info[0]['user']['followed_by']['count']
                        if self.is_self_checking is not False:
                            self.self_following = follows
                            self.self_follower = follower
                            self.is_self_checking = False
                            self.is_checked = True
                            return 0
                        media = user_info[0]['user']['media']['count']
                        follow_viewer = user_info[0]['user']['follows_viewer']
                        followed_by_viewer = user_info[0]['user']['followed_by_viewer']
                        requested_by_viewer = user_info[0]['user']['requested_by_viewer']
                        has_requested_viewer = user_info[0]['user']['has_requested_viewer']
                        log_string = "Follower : %i" % (follower)
                        self.write_log(log_string)
                        log_string = "Following : %s" % (follows)
                        self.write_log(log_string)
                        log_string = "Media : %i" % (media)
                        self.write_log(log_string)
                        if follower/follows > 2:
                            self.is_selebgram = True
                            self.is_fake_account = False
                            print('   >>>This is probably Selebgram account')
                        elif follows/follower > 2:
                            self.is_fake_account = True
                            self.is_selebgram = False
                            print('   >>>This is probably Fake account')
                        else:
                            self.is_selebgram = False
                            self.is_fake_account = False
                            print('   >>>This is a normal account')
                            
                        if follows/media < 10 and follower/media < 10:
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
                            filename = "photos/"+self.user_login+"/"+self.current_user+".jpg"
                            """
                            try:
                                f = open(filename)
                                f.close()
                                print('=============>>>file is exists bro!!!!')
                            except:
                                urllib.urlretrieve(user_info[0]['user']['profile_pic_url_hd'],filename)
                                print('=============>>>'+self.current_user+" profile pic is downloaded")
                            """
                        else:
                            self.is_following = False
                            print('   >>>You are NOT following this account')
                        self.is_checked = True
                        i+=1
                except:
                    self.media_by_tag = []
                    self.write_log("Except on get_info!")
                    time.sleep(20)
                    return 0
            else:
                return 0
  


    def get_media_id_user_feed (self):

        if (self.login_status):
            now_time = datetime.datetime.now()
            if self.is_by_tag != True :
                log_string = "======> Get media id by user: %s <====== \n%s" % (self.current_user,now_time.strftime("%d.%m.%Y %H:%M"))
                if self.is_checked != True :
                    self.get_user_info(self.current_user)
                if self.is_fake_account!=True and self.is_active_user!=False and self.is_selebgram!=True or self.is_by_tag !=False:
                    url_tag = 'https://www.instagram.com/%s%s' % (self.current_user, '/')
            else :
                log_string = "======> Get media id by Tag <======"
                url_tag = 'https://www.instagram.com/explore/tags/%s' % (random.choice(self.tag_list))
            self.write_log(log_string)
          
            if self.login_status == 1 and self.is_fake_account!=True and self.is_active_user!=False and self.is_selebgram!=True or self.is_by_tag !=False :

                try:
                    r = self.s.get(url_tag)
                    text = r.text

                    finder_text_start = ('<script type="text/javascript">'
                                         'window._sharedData = ')
                    finder_text_start_len = len(finder_text_start)-1
                    finder_text_end = ';</script>'

                    all_data_start = text.find(finder_text_start)
                    all_data_end = text.find(finder_text_end, all_data_start + 1)
                    json_str = text[(all_data_start + finder_text_start_len + 1) \
                                   : all_data_end]
                    all_data = json.loads(json_str)
             
                    if self.is_by_tag!= True :
                        self.media_by_user = list(all_data['entry_data']['ProfilePage'][0]\
                                            ['user']['media']['nodes'])
                    else :
                        self.media_by_tag = list(all_data['entry_data']['TagPage'][0]\
                                            ['tag']['media']['nodes'])
                    log_string="Get media by user success!"
                    self.write_log(log_string)
                except:
                    self.media_by_user = []
                    self.media_by_tag = []
                    self.write_log("XXXXXXX Except on get_media! XXXXXXX")
                    time.sleep(60)
                    return 0
            else:
                log_string = "Reject this account \n=================== \nReason : \n   Is Selebgram : %s \n   Is Fake Account : %s \n   Is Active User : %s \n" % (self.is_selebgram, self.is_fake_account, self.is_active_user)
                self.write_log(log_string)
                self.is_rejected = True
                self.media_by_tag = []
                self.media_by_user = []
                return 0

    def get_media_id_recent_feed (self):
        """ Get media ID set, by your hashtag """

        if (self.login_status):
            now_time = datetime.datetime.now()
            log_string = "%s : Get media id on recent feed \n%s"%(self.user_login,now_time.strftime("%d.%m.%Y %H:%M"))
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = 'https://www.instagram.com/#'
                try:
                    r = self.s.get(url_tag)
                    text = r.text
                    finder_text_start = ('<script type="text/javascript">'
                                         'window._sharedData = ')
                    finder_text_start_len = len(finder_text_start)-1
                    finder_text_end = ';</script>'

                    all_data_start = text.find(finder_text_start)
                    all_data_end = text.find(finder_text_end, all_data_start + 1)
                    json_str = text[(all_data_start + finder_text_start_len + 1) \
                                   : all_data_end]
                    all_data = json.loads(json_str)

                    self.media_by_tag = list(all_data['entry_data']['FeedPage'][0]\
                                            ['feed']['media']['nodes'])
                    log_string="Media in recent feed = %i"%(len(self.media_by_tag))
                    self.write_log(log_string)
                except:
                    self.media_by_tag = []
                    self.write_log("Except on get_media!")
                    time.sleep(20)
                    return 0
            else:
                return 0


    def get_user_id_post_page (self, code):
        """ Get media ID set, by your hashtag """

        if (self.login_status):
            now_time = datetime.datetime.now()
            log_string = "Get user id on post page \n%s"%(now_time.strftime("%d.%m.%Y %H:%M"))
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = 'https://www.instagram.com/p/%s/'%(code)
                try:
                    r = self.s.get(url_tag)
                    text = r.text
                    finder_text_start = ('<script type="text/javascript">'
                                         'window._sharedData = ')
                    finder_text_start_len = len(finder_text_start)-1
                    finder_text_end = ';</script>'

                    all_data_start = text.find(finder_text_start)
                    all_data_end = text.find(finder_text_end, all_data_start + 1)
                    json_str = text[(all_data_start + finder_text_start_len + 1) \
                                   : all_data_end]
                    all_data = json.loads(json_str)

                    self.user_list = list(all_data['entry_data']['PostPage'][0]\
                                            ['media']['likes']['nodes'])
                    log_string="User likes this post = %i"%(self.media_by_user[self.current_index]['likes']['count'])
                    self.write_log(log_string)
                except:
                    self.media_by_tag = []
                    self.write_log("Except on get_media!")
                    time.sleep(20)
                    return 0
            else:
                return 0

    def write_log(self, log_text):
        """ Write log by print() or logger """

        if self.log_mod == 0:
            try:
                print(self.user_login +" : "+ log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")
        elif self.log_mod == 1:
            # Create log_file if not exist.
            if self.log_file == 0:
                self.log_file = 1
                now_time = datetime.datetime.now()
                self.log_full_path = '%s%s_%s.log' % (self.log_file_path,
                                     self.user_login,
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
