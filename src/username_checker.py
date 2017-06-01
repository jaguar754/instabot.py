#!/usr/bin/env python
# -*- coding: utf-8 -*-
def username_checker(self):
    chooser = 0
    while len(self.user_list) > 0 and chooser < len(self.user_list):
        self.current_user = self.user_list[chooser]["user"]["username"]
        self.current_id = self.user_list[chooser]["user"]["id"]
        for index in range(len(self.unwanted_username_list)):
            if self.unwanted_username_list[index] in self.current_user:
                print('Username = ' + self.current_user + '\n      ID = ' +
                      self.current_id + '      <<< rejected ' +
                      self.unwanted_username_list[index] + ' is found!!!')
                break
        else:
            for index in range(len(self.user_info_list)):
                if self.current_user in self.user_info_list[index][0]:
                    print(
                        'Username = ' + self.current_user + '\n      ID = ' +
                        self.current_id +
                        '      <<< rejected this user is already in user info list!!!'
                    )
                    break
            else:
                print('Username = ' + self.current_user + '\n      ID = ' +
                      self.current_id + '      <<< added to user info list')
                self.user_info_list.append(
                    [self.current_user, self.current_id])
        chooser += 1
    log_string = "\nSize of user info list : %i Size of ex user list : %i \n" % (
        len(self.user_info_list), len(self.ex_user_list))
    self.write_log(log_string)
