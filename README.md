# InstaBot
Instagram bot. It works without instagram api, need only login and password. Write on python.

After Instagram [close api][1] (new review process), there were some problem, to make auto - like, comment and follow.

If your app can't pass new review process, this is solution! 

This InstaBot work by [https://www.instagram.com][2] and need only your login and password.
# Usage
Login:
--------------------
bot = InstaBot('login', 'password')

You can like one tag: 
--------------------
Set tag to like: bot.get_media_id_by_tag('dog')

Like 4 times: bot.like_all_exist_media(4)

Ore you can choose auto_mod (like all tags from setting by loop):
--------------------
Set tag list: bot.tag_list = ['moto', 'atv', 'car', 'travel', 'cat']

Start auto_mod: bot.auto_mod()

Logout from exist session:
--------------------
bot.logout()

[1]: http://developers.instagram.com/post/133424514006/instagram-platform-update
[2]: https://www.instagram.com
