#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instabot import InstaBot

bot = InstaBot(login="my_username", password="my_password",
               like_per_day=1000,
               comments_per_day=0,
               tag_list=['follow4follow', 'f4f', 'cute'],
               max_like_for_one_tag=50,
               follow_per_day=150,
               follow_time=5*60*60,
               unfollow_per_day=150,
               unfollow_break_min=15,
               unfollow_break_max=30,
               log_mod=0)

bot.new_auto_mod()
