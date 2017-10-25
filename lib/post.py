import requests
from lib.configure import getSite as SITE
from lib.configure import WORD
from lib.configure import enableProxy as PROXY
from lib.proxy import *
from lib.cookie import *
from lib.headers import *
from lib.payload import *
from lib.replace import *

s = requests.Session()
print_lock = threading.Lock()

# Reads word list from file and adds each name to array words[]
fx = open(WORD_LIST(), 'r')
words = fx.read().split('\n')
fx.close()

cookie = get_cookie()
header = prepare_headers(cookie)
link = URLS[SITE()]

def postJob(item):
    word = words[item]
    payload = ready_payload(word)
    r = None
    if PROXY():
        pl = get_proxy_list()
        select_random_proxy(pl)
        if check_proxy():
            r = s.post(link, data=payload, headers=header, cookies=cookie, proxies=proxyDict)
        else:
            pl = get_proxy_list()
            select_random_proxy(pl)
            r = s.post(link, data=payload, headers=header, cookies=cookie, proxies=proxyDict)
    else:
        r = s.post(URLS[SITE()], data=payload, headers=header, cookies=cookie)
    with print_lock:
        log_result(r, word, link)

def threader():
    while True:
        item = q.get()
        postJob(item)
        q.task_done()

start = time.time()

q = Queue()
for x in range(THREADS()):
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

for item in range(words.__len__()):
    q.put(item)

q.join()

total = str(time.time()-start)
print("\n\nEntire job took: %s seconds" % total)