import requests
import random
import threading
from queue import Queue
import time
from lib.proxy import *
from lib.log import *
from lib.replace import *
from lib.cookie import *
from lib.payload import ready_payload
from lib.headers import prepare_headers
from lib.configure import enableProxy as PROXY
from lib.configure import getSite as SITE
from lib.configure import numThreads as THREADS
from lib.configure import getWordList as WORD_LIST

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
    if PROXY():
        plist = get_proxy_list()
        i = random.randrange(0, plist.__len__())
        sess = set_proxy(s, plist[i])
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
for x in range(THREADS()):
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

for item in range(words.__len__()):
    q.put(item)

q.join()

total = str(time.time()-start)
print("\nChecked %s words in %s seconds." % (words.__len__(), total))
