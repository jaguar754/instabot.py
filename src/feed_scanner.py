#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time

from .likers_graber_protocol import likers_graber_protocol
from .new_auto_mod_unfollow2 import new_auto_mod_unfollow2
from .recent_feed import get_media_id_recent_feed
from .user_feed import get_media_id_user_feed


def feed_scanner(self):
    #This is to limit how many people do you want to put into list before
    ##The bot start to check their profile one by one and start following them
    limit = random.randint(51, 90)
    while len(self.user_info_list) < limit:
        #First the bot try to collect media id on your recent feed
        get_media_id_recent_feed(self)
        #If your account is old enough, there will be 10 photos on your recent feed
        if len(self.media_on_feed) > 10:
            #Select the media on your recent feed randomly
            chooser = random.randint(0, len(self.media_on_feed) - 1)
            #The bot will save the owner of the media name and use it to try checking his/her profile
            self.current_user = self.media_on_feed[chooser]["node"]["owner"][
                "username"]
            self.current_id = self.media_on_feed[chooser]["node"]["owner"][
                "id"]

        #If your account is new, and you don't following anyone, your recent feed will be empty
        else:
            #If your recent feed is empty, then you start collecting media id by hashtag
            self.is_by_tag = True
            get_media_id_user_feed(self)
            max_media = 0
            while len(self.media_on_feed) > 5 and max_media < 5:
                chooser = random.randint(0, len(self.media_on_feed) - 1)
                self.current_id = self.media_on_feed[chooser]["node"]["owner"][
                    "id"]
                self.follow(self.current_id)
                self.media_on_feed[chooser] = None
                max_media += 1
                time.sleep(30)
            self.is_by_tag = False
            self.media_on_feed = []
        if len(self.user_info_list) < 10000:
            for index in range(len(self.ex_user_list)):
                if self.ex_user_list[index][0] in self.current_user:
                    print(
                        '============================== \nUpss ' +
                        self.current_user +
                        ' is already in ex user list... \n=============================='
                    )
                    break
            else:
                likers_graber_protocol(self)
                self.ex_user_list.append([self.current_user, self.current_id])
            self.user_list = []
            self.media_by_user = []
            self.media_on_feed = []

        if len(self.ex_user_list) > 20:
            chooser = random.randint(0, len(self.ex_user_list) - 1)
            self.current_user = self.ex_user_list[chooser][0]
            self.current_id = self.ex_user_list[chooser][1]
            print('Trying to unfollow : ' + self.current_user)
            new_auto_mod_unfollow2(self)
            del self.ex_user_list[chooser]
        time.sleep(random.randint(15, 22))
