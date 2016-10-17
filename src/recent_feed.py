#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import json

def get_media_id_recent_feed (self):
    if (self.login_status) :
        now_time = datetime.datetime.now()
        log_string = "%s : Get media id on recent feed \n %s" % (self.user_login, now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        url = 'https://www.instagram.com/#'
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

            self.media_on_feed = list(all_data['entry_data']['FeedPage'][0]\
                                         ['feed']['media']['nodes'])
            log_string="Media in recent feed = %i"%(len(self.media_on_feed))
            self.write_log(log_string)
        except:
            self.media_on_feed = []
            self.write_log('Except on get media!!')
            time.sleep(20)
            return 0 
    else:
        return 0 
