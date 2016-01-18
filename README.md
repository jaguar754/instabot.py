# InstaBot
Instagram bot. It works without instagram api, need only login and password. Write on python.
# Usage

bot = InstaBot('login', 'password')
# You can like one tag: 
bot.get_media_id_by_tag('dog') - set tag to like.
bot.like_all_exist_media(4) - like 4 times.

# Ore you can choose auto_mod (like all tags from setting by loop).
# Set tag list:
bot.tag_list = ['moto', 'atv', 'car', 'travel', 'cat']
# Start auto_mod:
bot.auto_mod()

# Logout from exist session
bot.logout()
