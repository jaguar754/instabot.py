def new_like_all_exist_media(self):
    i = self.current_index
    # Media count by this user.
    l_c = self.media_by_user[i]['likes']['count']
    if l_c <= self.media_max_like and l_c >= self.media_min_like:
        log_string = "Trying to like media: %s" %\
                      (self.media_by_user[i]['id'])
        self.write_log(log_string)
        like = self.like(self.media_by_user[i]['id'])
        if like != 0:
            if like.status_code == 200:
                log_string = "Liked: %s. Likes: #%i." %\
                              (self.media_by_user[i]['id'],
                               self.media_by_user[i]['likes']['count'])
                self.write_log(log_string)
            elif like.status_code == 400:
                log_string = "Not liked: %i" \
                              % (like.status_code)
                self.write_log(log_string)
            else:
                log_string = "Not liked: %i" \
                              % (like.status_code)
                self.write_log(log_string)
                return False
        else:
            return False
    else:
        print('Too much liker for this media!!! LC = %i' % (l_c))
        return True
