from instabot import InstaBot
from userinfo import UserInfo
import time
import random

#use userinfo
ui = UserInfo()
ui.search_user(user_name="login")

#take followers
ui.get_following()
followers = ui.following

#favorite id list
favorites = ['111','222','333']

#some lists
newlist = []
endlist = []

#get followers id
for item in followers:
    newlist.append(item['id'])
    
#create final list
for ids in newlist:
        if ids not in favorites:
            endlist.append(ids)

#use instabot
bot = InstaBot('login', 'password')

print ('Number of unnecessary subscriptions:',len(endlist),'\n')

for items in endlist:
    rnd = random.randint(1,16)
    bot.unfollow(items)
    print ('Wait',30+rnd,'sec')
    time.sleep(30+rnd)

print ('All done.')

