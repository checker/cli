import requests
import random
import threading
from queue import Queue
import time
from lib.log import log_result
from lib.replace import URLS
from lib.cookie import get_cookie
from lib.payload import ready_payload
from lib.headers import prepare_headers

from lib.ConfigHelper import ConfigHelper
from lib.ProxyHelper import ProxyHelper

ch = ConfigHelper()
ph = ProxyHelper()

print_lock = threading.Lock()

words = ch.getWords()

cookie = get_cookie()
header = prepare_headers(cookie)
link = URLS[ch.getSite()]

def postJob(item):
    word = words[item]
    payload = ready_payload(word)
    s = requests.Session()
    if ch.enableProxy():
        plist = ch.getProxies()
        i = random.randrange(0, plist.__len__())
        sess = ph.setProxy(s, plist[i])
        r = sess.post(link, data=payload, headers=header, cookies=cookie)
    else:
        r = s.post(link, data=payload, headers=header, cookies=cookie)
    with print_lock:
        log_result(r, word, link)

def threader():
    while True:
        item = q.get()
        postJob(item)
        q.task_done()

start = time.time()

q = Queue()
print("Starting up threads...")
for x in range(ch.numThreads()):
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()
    print("[Thread-%d] has started." % x)

for item in range(words.__len__()):
    q.put(item)

q.join()

total = str(time.time()-start)
print("\nChecked %s words in %s seconds." % (words.__len__(), total))
