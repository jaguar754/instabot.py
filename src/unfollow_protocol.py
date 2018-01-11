#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

from .follow_protocol import follow_protocol
from .new_auto_mod_unfollow2 import new_auto_mod_unfollow2
from .recent_feed import get_media_id_recent_feed
from .user_feed_protocol import user_feed_protocol


def unfollow_protocol(self):
    limit = random.randint(10, 22) + 1
    while self.unfollow_counter <= limit:
        get_media_id_recent_feed(self)
        if len(self.media_on_feed) == 0:
            self.follow_counter = 0
            follow_protocol(self)
        if len(self.media_on_feed) != 0 and self.is_follower_number < 5:
            chooser = random.randint(0, len(self.media_on_feed) - 1)
            self.current_user = self.media_on_feed[chooser]["node"]["owner"][
                "username"]
            self.current_id = self.media_on_feed[chooser]["node"]["owner"][
                "id"]
            if self.bot_mode == 2:
                new_auto_mod_unfollow2(self)
                time.sleep(30)
                return
            user_feed_protocol(self)
            self.like_counter = 0
            self.media_by_user = []
            if self.is_selebgram is not False or self.is_fake_account is not False or self.is_active_user is not True or self.is_follower is not True:
                new_auto_mod_unfollow2(self)
                try:
                    del self.media_on_feed[chooser]
                except:
                    self.media_on_feed = []
        else:
            follow_protocol(self)
            self.is_follower_number = 0
            time.sleep(13 + 5)
