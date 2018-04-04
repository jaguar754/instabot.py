#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .user_info import get_user_info


def check_status(self):
    self.is_self_checking = True
    self.is_checked = False
    while self.is_checked != True:
        get_user_info(self, self.user_login)
    self.like_counter = 0
    self.follow_counter = 0
    self.unfollow_counter = 0
