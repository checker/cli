import requests
import random
import threading
from queue import Queue
import time
from lib.log import log_result
from lib.replace import replace
from lib.ConfigHelper import ConfigHelper
from lib.ProxyHelper import ProxyHelper

ch = ConfigHelper()
ph = ProxyHelper()

print_lock = threading.Lock()
words = ch.getWords()

def requestJob(item):
    word = words[item]

    if ch.getSite()==3 and not 4<len(word)<16:
        with print_lock:
            print("["+threading.current_thread().name+"] "+word+" is UNAVAILABLE on twitter because it has illegal length.")
    elif ch.getSite()==10 and not len(word)<40:
        with print_lock:
            print("["+threading.current_thread().name+"] "+word+" is UNAVAILABLE on github because it has illegal length.")
    elif ch.getSite()==13 and not 2<len(word)<21:
        with print_lock:
            print("["+threading.current_thread().name+"] "+word+" is UNAVAILABLE on pastebin because it has illegal length.")
    else:
        link = replace(word)
        s = requests.Session()
        if ch.enableProxy():
            plist = ch.getProxies()
            i = random.randrange(0, plist.__len__())
            sess = ph.setProxy(s, plist[i])
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
for x in range(ch.numThreads()):
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

for item in range(words.__len__()):
    q.put(item)

q.join()

total = str(time.time()-start)
print("\nChecked %s words in %s seconds." % (words.__len__(), total))
