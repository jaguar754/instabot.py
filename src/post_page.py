#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time

def get_user_id_post_page (self, code):
    if (self.login_status):
        log_string = 'Get user id on post page'
        self.write_log(log_string)
        url = 'https://www.instagram.com/p/%s/'%(code)
        try:
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

            self.user_list = list(all_data['entry_data']['PostPage'][0]\
                                            ['media']['likes']['nodes'])
            log_string="User likes this post = %i"%(self.media_by_user[self.current_index]['likes']['count'])
            self.write_log(log_string)
        except:
            self.media_on_feed = []
            self.write_log("Except on get user list!!!!")
            time.sleep(10)
            return 0
    else:
        return 0
