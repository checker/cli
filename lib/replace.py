import re
from lib.configure import PLACEHOLDER
from lib.configure import getCustomUrl as URL
from lib.configure import getSite as SITE

# Site URLs
URLS = {
    1:URL,
    2:"https://api.mojang.com/users/profiles/minecraft/%s",
    3:"https://api.twitter.com/i/users/username_available.json?username=%s",
    4:"http://www.instagramavailability.com/_validate_username?username=%s",
    5:"https://steamcommunity.com/id/%s",
    6:"https://steamcommunity.com/groups/%s",
    7:"https://soundcloud.com/%s",
    8:"https://passport.twitch.tv/usernames/%s",
    9:"https://mixer.com/api/v1/channels/%s",
    10:"https://github.com/%s",
    11:"https://about.me/%s",
    12:"https://youtube.com/%s"
}


def replace(word):
    # Finds and replaces matches of the name variable with the actual word to insert in URL
    if SITE() == 1:
        x = re.sub(PLACEHOLDER, word, URLS[1])
        return x
    else:
        return URLS[SITE()] % word
    