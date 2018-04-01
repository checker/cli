import requests
import random
import threading
from queue import Queue
import time
from lib.ProxyHelper import ProxyHelper
from lib.log import log_result
from lib.replace import replace
from lib.configure import enableProxy as PROXY
from lib.configure import getProxyList as PROXYLIST
from lib.configure import getSite as SITE
from lib.configure import numThreads as THREADS
from lib.configure import getWordList as WORD_LIST

print_lock = threading.Lock()

# Reads word list from file and adds each name to array words[]
fx = open(WORD_LIST(), 'r')
words = fx.read().split('\n')
fx.close()

def requestJob(item):
    word = words[item]
    link = replace(word)
    s = requests.Session()
    if PROXY() == "True":
        plist = PROXYLIST()
        i = random.randrange(0, plist.__len__())
        sess = ProxyHelper().setProxy(s, plist[i])
        r = sess.get(link)
    else:
        r = s.get(link)
    with print_lock:
        log_result(r, word, link)

def threader():
    while True:
        item = q.get()
        requestJob(item)
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
