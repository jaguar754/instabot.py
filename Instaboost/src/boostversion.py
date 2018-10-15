#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

def boostversion(self):

    s = requests.Session()
    try:
        r = s.get('https://github.com/andrewsegas/docs/blob/master/boostv2')
        
        if r.status_code == 200:
            self.boostUpdated = True
        else:
            self.boostUpdated = False
    except:
        print("Exception on Check Version")
        self.boostUpdated = True