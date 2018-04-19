#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

def boostversion(self):

    s = requests.Session()
    try:
        r = s.get('http://ec2-18-218-101-210.us-east-2.compute.amazonaws.com:8080/?user='+self.user_login+'&version='+self.boostVersion)
        finder = r.text.find(self.boostVersion)
        if finder != -1:
            self.boostUpdated = True
        else:
            self.boostUpdated = False
    except:
        print("Exception on Check Version")
        self.boostUpdated = True