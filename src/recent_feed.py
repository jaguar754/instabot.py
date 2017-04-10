#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import time


def get_media_id_recent_feed(self):
    if self.login_status:
        now_time = datetime.datetime.now()
        log_string = "%s : Get media id on recent feed \n %s" % (
            self.user_login, now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        url = 'https://www.instagram.com/?__a=1'
        try:
            r = self.s.get(url)
            all_data = json.loads(r.text)

            self.media_on_feed = list(all_data['graphql']['user']['edge_web_feed_timeline']['edges'])
            log_string = "Media in recent feed = %i" % (
                len(self.media_on_feed))
            self.write_log(log_string)
        except:
            self.media_on_feed = []
            self.write_log('Except on get media!!')
            time.sleep(20)
            return 0
    else:
        return 0
