import requests
from lib.configure import getProxyList as PROXYLIST
from lib.configure import enableProxy as PROXY

ps = requests.Session()

good_proxies = []
bad_proxies = []

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

def set_proxy(session, proxy):
    if proxy != 'none':
        session.proxies.update({
            'http:' : 'http://' + proxy,
            'https:' : 'https://' + proxy
        })
    return session

def check_proxy(proxy):
    try:
        session = set_proxy(ps, proxy)
        r = session.get('https://google.com', timeout=4)
        if r.status_code is 200:
            good_proxies.append(proxy)
            return True
    except r.raise_for_status():
        bad_proxies.append(proxy)
        return False
