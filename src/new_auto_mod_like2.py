#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from .new_auto_mod_likeall import new_like_all_exist_media


def new_auto_mod_like2(self):
    if len(self.media_by_user) > 0:
        # You have media_id to like:
        self.current_index = random.randint(0, len(self.media_by_user) - 1)
        log_string = "Current Index = %i of %i medias" % (
            self.current_index, len(self.media_by_user))
        self.write_log(log_string)

        new_like_all_exist_media(self)
        # Del first media_id
        del self.media_by_user[self.current_index]
