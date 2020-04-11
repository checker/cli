import os
import threading
from queue import Queue
import time
import requests
from lib.ConfigHelper import ConfigHelper

ch = ConfigHelper()

class ProxyHelper():

    def __init__(self):
        self.session = requests.Session()
        self.proxies = ch.getProxies()
        self.numProxies = len(ch.getProxies())
        self.print_lock = threading.Lock()
        self.queue = Queue()
        self.good = []
        self.bad = []

    def checkJob(self, proxy):
        #sess = self.setProxy(self.session, proxy)
        proxyDict = {
            'http:' : proxy,
            'https:' : proxy,
            'socks' : proxy
        }
        try:
            r = self.session.get('https://google.com', timeout=4, proxies=proxyDict)
            if r.status_code == 200:
                self.good.append(proxy)
                with self.print_lock:
                    print("%s is working..." % proxy)
            else:
                raise Exception("Bad Proxy!")
        except Exception as error:
            self.bad.append(proxy)
            print(error)
            

    def threader(self):
        while True:
            item = self.queue.get()
            self.checkJob(item)
            self.queue.task_done()
    
    def setProxy(self, session, proxy):
        if proxy is not None:
            session.proxies.update({
                'http:' : proxy,
                'https:' : proxy,
                'socks' : proxy
            })
        return session

    def checkProxies(self):
        
        print("Checking and filtering out bad proxies...")
        start = time.time()

        print("Starting up threads...")
        for x in range(ch.numThreads()):
            t = threading.Thread(target = self.threader)
            t.daemon = True
            t.start()
            print("[Thread-%d] has started." % x)

        for item in self.proxies:
            self.queue.put(item)

        self.queue.join()
        print("Done.")

        gp = open('proxy_lists/good_proxies.txt', 'a')
        for p in self.good:
            gp.write("%s\n" % str(p))
        gp.close()

        bp = open('proxy_lists/bad_proxies.txt', 'a')
        for p in self.bad:
            bp.write("%s\n" % str(p))
        bp.close()

        total = str(time.time()-start)
        numBad = len(self.bad)
        print("\nSearched %s proxies and filtered out %s bad proxies in %s seconds" % (self.numProxies, numBad, total))

        path = "proxy_lists/%s" % ch.getProxies(filename_only=True)
        os.remove(path)
        os.rename('proxy_lists/good_proxies.txt', path)
