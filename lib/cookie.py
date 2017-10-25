import requests
from lib.configure import getSite as SITE

s = requests.Session()

def get_cookie():
    r = s.get(URLS[SITE()])
    return r.cookies