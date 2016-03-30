## InstaBot
Instagram bot v 1.0. It works without instagram [api][1](the new review process), needs only login and password that is not stored anywhere online. Only local. Written in Python

<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=UM6L3YJENAQZ6&lc=US&item_name=InstaBot%2epy&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted" title="Buy me a beer"><img src="http://www.mikkonen.info/polaroid_gallery/images/paypal_beer.png"></a>

## Requirements
`Python2.7` minimum
A working Instagram account
(`instabot.py` file must be in `UTF-8` encoding if you use `Python 3`, or `ASCII` in `Python 2` ([PEP][3])!)

## Usage
#### Example of usage:
For example see `example.py`. Just change the login and password information with your own, then run `example.py` and the bot will start doing it's magic!

####1) Login:
Login automatic, as followed, by creating the `InstaBot` class element:
```python
bot = InstaBot('login', 'password',
                like_per_day=1000,
                media_max_like=10,
                media_min_like=0,
                follow_per_day=0,
                follow_time=5*60*60,
                unfollow_per_day=0,
                comments_per_day=0,
                tag_list=['cat', 'car', 'dog'],
                max_like_for_one_tag = 5,
                log_mod = 0)
```

| Parameter            | Type|                Description                           |        Default value             |                 Example value                   |
|:--------------------:|:---:|:----------------------------------------------------:|:--------------------------------:|:-----------------------------------------------:|
| login                | str | your instagram username                              |                                  | python_god                                      |
| password             | str | your instagram password                              |                                  | python_god_password                             |
| like_per_day         | int | how many likes the bot does in 1 day                 | 1000                             | 500                                             |
| media_max_like       | int | don't like if media has more than ... likes          | 10                               | 100                                             |
| media_min_like       | int | don't like if media has less than ... likes          | 0                                | 5                                               |
| follow_per_day       | int | how many users to follow in 1 day                    | 0                                | 100                                             |
| follow_time          | int | how many times passes before the  bot unfollows a followed user | 5*60*60                          | 60*60                                           |
| unfollow_per_day     | int | how many user unfollows the bot does in day          | 0                                | 100                                             |
| comments_per_day     | int | how many comments the bot writes in a day       | 0                                | 50                                              |
| tag_list             | list| list of tag the bot uses                             | ['cat', 'car', 'dog']            | ['moto', 'girl', 'python']                      |
| max_like_for_one_tag | int | bot get 21 media from one tag, how many use by row   | 5                                | 10                                              |
| log_mod              | int | logging mod                                          | 0                                | 0 log to console, 1 log to file, 2 no log.      |


####2) Set likes and unlike:
How many likes set bot in one day. Default value is 1000 likes per 24 hours.
If you want to do more than 1000 likes in day - instagram can ban you.
Usually this bot is used 24/7 and it's default setup to distripute 1000 likes in day evenly. If you want more likes in one moment, set this parameter to 5000 or 10000 or more. Formula: set like with delay = `(24 hour * 60 minute * 60 second / like_per_day)`
######Be careful, don't set more than 1000 like in day or you can be banned! Be warned!!
```python
like_per_day=1000
```
Don't like media (photo or video) if it have more than `media_max_like` likes. `media_max_like = 0` will ignore this property. If media have too much likes - your like have not feedback.
Don't like media (photo or video) if it have less than `media_min_like` likes. `media_min_like = 0` will ignore this property.
```python
media_max_like=10
media_min_like=0
```
Tag list to like.
```python
tag_list = ['cat', 'car', 'dog']
```
Like 1 to `max_like_for_one_tag` times by row.
```python
max_like_for_one_tag=5
```

You can like one tag:
```python
bot.get_media_id_by_tag('dog')
```
Like 4 times:
```python
bot.like_all_exist_media(4)
```
Or you can choose `auto_mod` (like all tags from setting by loop):
```python
bot.auto_mod()
```
For unlike:
```python
bot.unlike('media_id')
```
####3) Set comments:
```python
bot.comment('media_id', 'comment')
```
For example:
```python
bot.comment(11111111111111111111, 'Cool!')
```
####4) Follow and unfollow:
Follow:
```python
bot.follow('user_id')
```
Unfollow:
```python
bot.unfollow('user_id')
```
For example (follow and unfollow user with id 111111111):
```python
bot.follow(111111111)
bot.unfollow(111111111)
```
####5) Else:
Log mod: `log_mod=0` log to console, `log_mod=1` log to file, `log_mod=2` no log.
```python
log_mod = 0
```
####6) Logout from exist session:
```python
bot.logout()
```
## Usage examples
Standard use (will like by loop, all default tag):
```python
bot = InstaBot('login', 'password')
bot.auto_mod()
```
Standard use with your tag (will like by loop, all your tag):
```python
bot = InstaBot('login', 'password', tag_list = ['with', 'your', 'tag'])
bot.auto_mod()
```
Standard use with change default settings (you should know what you do!):
```python
bot = InstaBot('login', 'password',
               like_in_day=100000,
               media_max_like=50,
               media_min_like=5,
               tag_list = ['like', 'follow', 'girls'],
               max_like_for_one_tag=50,
               log_mod = 1)
bot.auto_mod()
```
Get media_id buy one tag `'python'` and like 4 of them:
```python
bot = InstaBot('login', 'password')
bot.get_media_id_by_tag('python')
bot.like_all_exist_media(4)
```

## How to install and run:
1) You should download and install `Python` on your OS.

2) You should install Python lib `requests`. Run command `pip3 install requests` if you use `Python 3`, or type `pip install requests` if you use `Python 2`.

3) Download `instabot.py` and save it in right encoding!

4) Add the code to the end of the file (like in usage examples), depending on how you want to use bot.

5) Run program `python3 instabot.py` or `python instabot.py` on MAC and Linux, or `python instabot.py` on Windows.
## Test on:
Windows & Python 3.4

CentOS & Python 3.4

CentOS & Python 2.6
## Warning!
The entire responsibility for the use of bot programs entirely on you.
#### What i see every time open instagram:
![What i see every time open instagram](http://cs627124.vk.me/v627124268/35d95/rSponlVRclY.jpg)

## Work with userinfo.py
If you want to get some user info (follower, following and etc.) Instagram don't give this info.
Class in `userinfo.py` aggregate this information, from other sites (now only from http://ink361.com/)
#### How to use:
```python
ui = UserInfo()
```
Search by `user_name` (need to get `user_id`, `user_name` if you don't know it):
```python
ui.search_user(user_name="danbilzerian")
```
or if you know `user_id` use `ui.search_user(user_id="50417061")`. Your result:
```python
print(ui.user_name)
print(ui.user_id)
```
Get following list with no limit
```python
ui.get_following()
print(ui.following)
```
Get followers list with limit 10:
```python
ui.get_followers(limit=10)
print(ui.followers)
```

[1]: http://developers.instagram.com/post/133424514006/instagram-platform-update
[2]: https://www.instagram.com
[3]: https://www.python.org/dev/peps/pep-0008/#source-file-encoding
