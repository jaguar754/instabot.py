#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time

from feed_scanner import feed_scanner
from user_info import get_user_info


def follow_protocol(self):
    limit = random.randint(5, 10)
    while self.follow_counter < limit:
        chooser = 0
        if len(self.user_info_list) > 0:
            chooser = random.randint(0, len(self.user_info_list) - 1)
            self.current_user = self.user_info_list[chooser][0]
            self.current_id = self.user_info_list[chooser][1]
            print('=============== \nCheck profile of ' + self.current_user +
                  '\n===============')
            get_user_info(self, self.current_user)
        else:
            print('xxxxxxx user info list is empty!!! xxxxxxxxx')
            feed_scanner(self)
        if self.is_selebgram != True and self.is_fake_account != True and self.is_active_user != False:
            if self.is_following != True:
                print('Trying to follow : ' + self.current_user +
                      ' with user ID :' + self.current_id)
                self.follow(self.current_id)
                print('delete ' + self.user_info_list[chooser][0] +
                      ' from user info list')
                del self.user_info_list[chooser]
        else:
            print('delete ' + self.user_info_list[chooser][0] +
                  ' from user info list')
            del self.user_info_list[chooser]

        time.sleep(random.randint(13, 26))
