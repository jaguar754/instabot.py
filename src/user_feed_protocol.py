#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time

from new_auto_mod_like2 import new_auto_mod_like2
from user_feed import get_media_id_user_feed


def user_feed_protocol(self):
    #To limit how many photos to scan
    limit = random.randint(4, 6)
    counterz = 0
    self.is_checked = False
    self.is_rejected = False
    while counterz <= limit:
        # ------------------- Get media_id -------------------
        if len(self.media_by_user) is 0:
            get_media_id_user_feed(self)
            # ------------------- Like -------------------
        if self.is_rejected is not False:
            return 0
        if self.is_follower is not False:
            print(
                "@@@@@@@@@@@@@@ This is your follower B****h!!! @@@@@@@@@@@@@")
            self.is_follower_number += 1
            time.sleep(5)
            return
        new_auto_mod_like2(self)
        counterz += 1
        time.sleep(3 * 15)
