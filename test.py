#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instabot import InstaBot
import time
import random

bot = InstaBot(login="username", password="password",
               tag_list=["cat"],
               log_mod=0)

#To check your current status
##Eg : check your following and follower number 
##before the bot makes some decisions
def check_status():
    bot.is_self_checking = True
    bot.is_checked = False
    while bot.is_checked != True:
        bot.get_user_info(bot.user_login)
    #Initialization
    bot.like_counter = 0
    bot.follow_counter = 0
    bot.unfollow_counter = 0
	
while True:
    print("###### Your Username Here :) ######")
    check_status()
    #If user account have more following than follower
    ##The bot will try to unfollowing people who don't follow back
    while bot.self_following - bot.self_follower > 200:
        bot.new_auto_mod2()
        time.sleep(10*60)
        check_status()

    #If user account have more followers than following
    ##The bot will try to collect account ID by scanning medias (photos or videos)
    ##The bot will open photos on your recent feed one by one
    ##If the media have 10 or more likes, the bot will collect
    ##accounts name who like those media and save it into list 
    while bot.self_following - bot.self_follower < 400:
        #The bot will put people who like photos from another account on your recent feed
        ##If the bot can't get more than 50 people, then it will keep scanning your recent feed
        while len(bot.user_info_list) <50 :
            #Method to scan your recent feed and put some account to follow later into list
            bot.new_auto_mod6()
            time.sleep(5*60)
            #After you have plenty of account in your list
            ##This method is used to do some protocol before the bot send follow request
            ##In this method, the bot will try to figure out what kind of people inside your list one by one
            bot.new_auto_mod4()
            time.sleep(10*60)
            #After following people, the bot will update your current status
            check_status()

