#!/usr/bin/env python3
# Python Standard Modules
import sys
import os
import threading
from queue import Queue
import time
from lib.proxy import *
from lib.configure import getSite as SITE
from lib.configure import enableProxy as PROXY
from lib.configure import numThreads as THREADS
from lib.configure import getProxyList as PROXYLIST
from lib.configure import getBadProxyList as BADPROXYLIST

print_lock = threading.Lock()
plist = get_proxy_list()
numProxies = len(plist)
q = Queue()

def requestJob(proxy):
    if check_proxy(proxy):
        with print_lock:
            print("%s is working" % proxy)

def threader():
    while True:
        item = q.get()
        requestJob(item)
        q.task_done()

def main():
    if PROXY and plist is not None:
        print("Checking and filtering out bad proxies...")
        start = time.time()

        for x in range(THREADS()):
            t = threading.Thread(target = threader)
            t.daemon = True
            t.start()

        for item in plist:
            q.put(item)

        q.join()

        f = open('proxy_lists/good_proxies.txt', 'a')
        for p in good_proxies:
            f.write("%s\n" % str(p))
        f.close()

        f = open('proxy_lists/bad_proxies.txt', 'a')
        for p in bad_proxies:
            f.write("%s\n" % str(p))
        f.close()

        total = str(time.time()-start)
        numBad = len(bad_proxies)
        print("\nSearched %s numProxies and filtered out %s bad proxies in %s seconds" % (numProxies ,numBad, total))

    if (SITE() == 5) or (SITE() == 6): # Steam
        import lib.parse
    elif SITE() == 4:
        import lib.post
    else:
        import lib.get

    os.remove(PROXYLIST())
    os.rename('proxy_lists/good_proxies.txt', PROXYLIST())

if __name__ == "__main__":
    main()
