import requests
from lib.replace import *
from lib.ConfigHelper import ConfigHelper
from lib.ProxyHelper import ProxyHelper

ch = ConfigHelper()
ph = ProxyHelper()

s = requests.Session()

def get_cookie():
    r = s.get(URLS[ch.getSite()])
    return r.cookies