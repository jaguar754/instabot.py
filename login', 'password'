## InstaBot
Instagram bot. It works without instagram api, need only login and password. Write on python.

After Instagram [close api][1] (new review process), there were some problem, to make auto - like, comment and follow.

If your app can't pass new review process, this is solution!

This InstaBot work by [https://www.instagram.com][2] and need only your login and password.
## Usage
####1) Login:
Login automatic, when you create `InstaBot` class element:
```python
bot = InstaBot('login', 'password',
               like_per_day=1000,
               more_than_likes=10,
               tag_list = ['cat', 'car', 'dog'],
               max_like_for_one_tag=5,
               log_mod = 0)
```
####2) Set likes:
How many likes set bot in one day.
```python
like_per_day=1000
```
Don't like media (photo or video) if it have more than `more_than_likes` likes. If media have too much likes - your like have not feedback.
```python
more_than_likes=10
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
Standard use with change defaul settings (you should know what you do!):
```python
bot = InstaBot('login', 'password',
               like_in_day=100000,
               more_than_likes=5,
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
## Requirements
`Python`

Instagram account

`instabot.py` file must be in `UTF-8` encoding if you use `Python 3`, or `ASCII` in `Python 2` ([PEP][3])!
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

[1]: http://developers.instagram.com/post/133424514006/instagram-platform-update
[2]: https://www.instagram.com
[3]: https://www.python.org/dev/peps/pep-0008/#source-file-encoding
