import random
import requests
from lib.configure import getProxyList as PROXYLIST
from lib.configure import enableProxy as PROXY
from lib.configure import getProtocol as PROTOCOL

proxyDict = {}

def get_proxy_list():
    if PROXY() and (PROXYLIST() != None):
        fx = open(PROXYLIST(), 'r')
        proxies = fx.read().split('\n')
        fx.close()

        return proxies
    else:
        if not PROXY():
            print("Proxy support is disabled. Please enable it in the config.")
        elif PROXYLIST() == []:
            print("No proxies available to use.")

def select_random_proxy(plist):
    i = random.randrange(0, plist.__len__())
    proxyDict[PROTOCOL()] = "http://" + str(plist[i])

def check_proxy():
    try:
        requests.get(
            "https://google.com",
            proxies=proxyDict
        )
    except IOError:
        print("Proxy failed, trying another...")
        return False
    else:
        return True