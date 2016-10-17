#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import json
import random

def get_user_info (self, username):
    if (self.login_status):
        now_time = datetime.datetime.now()
        log_string = "%s : Get user info \n%s"%(self.user_login,now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        if self.login_status == 1:
            url = 'https://www.instagram.com/%s/'%(username)
            try :
                r = self.s.get(url)
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
              	
                log_string="Checking user info.."
                self.write_log(log_string)

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
                else:
                    self.is_following = False
                    print('   >>>You are NOT following this account')
                    self.is_checked = True
            except:
                self.media_on_feed = []
                self.write_log("Except on get_info!")
                time.sleep(20)
                return 0
        else:
            return 0
