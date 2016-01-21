# InstaBot
Instagram bot. It works without instagram api, need only login and password. Write on python.

After Instagram [close api][1] (new review process), there were some problem, to make auto - like, comment and follow.

If your app can't pass new review process, this is solution! 

This InstaBot work by [https://www.instagram.com][2] and need only your login and password.
# Usage
Login:
--------------------
```python
bot = InstaBot('login', 'password', 
               like_in_day=1000,
               more_than_likes=10,
               tag_list = ['cat', 'car', 'dog'],
               max_like_for_one_tag=5,
               log_mod = 0)
```
How many likes set bot in one day.
```python
like_in_day=100
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
Log mod: `log_mod=0` log to console, `log_mod=1` log to file, `log_mod=2` no log.
```python
log_mod = 0
```
You can like one tag: 
--------------------
Set tag to like: 
```python
bot.get_media_id_by_tag('dog')
```
Like 4 times: 
```python
bot.like_all_exist_media(4)
```
Or you can choose `auto_mod` (like all tags from setting by loop):
--------------------
Start auto_mod: 
```python
bot.auto_mod()
```
Logout from exist session:
--------------------
```python
bot.logout()
```

# Usage examples
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
# Requirements
Python 3.4 +

.py file must be in UTF-8 encoding!
# Test on:
Windows 8 & Python 3.4

CentOS 6 & Python 3.4
[1]: http://developers.instagram.com/post/133424514006/instagram-platform-update
[2]: https://www.instagram.com
