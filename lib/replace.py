import re
from lib.ConfigHelper import ConfigHelper, PLACEHOLDER

ch = ConfigHelper()

# Site URLs
URLS = {
    1:ch.getCustomUrl(),
    2:"https://api.mojang.com/users/profiles/minecraft/%s",
    3:"https://api.twitter.com/i/users/username_available.json?username=%s",
    4:"https://instagram.com/accounts/web_create_ajax/attempt/",
    5:"https://steamcommunity.com/id/%s",
    6:"https://steamcommunity.com/groups/%s",
    7:"https://soundcloud.com/%s",
    8:"https://passport.twitch.tv/usernames/%s",
    9:"https://mixer.com/api/v1/channels/%s",
    10:"https://github.com/%s",
    11:"https://about.me/%s",
    12:"https://youtube.com/c/%s",
    13:"http://pastebin.com/u/%s",
    14:"https://giphy.com/channel/%s"
}


def replace(word):
    # Finds and replaces matches of the name variable with the actual word to insert in URL
    if ch.getSite() == 1:
        x = re.sub(PLACEHOLDER, word, URLS[1])
        return x
    else:
        return URLS[ch.getSite()] % word
    