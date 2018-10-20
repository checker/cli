from bs4 import BeautifulSoup
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

def parseJob(item):
    word = words[item]
    link = replace(word)
    s = requests.Session()
    if ch.enableProxy():
        plist = ch.getProxies()
        i = random.randrange(0, plist.__len__())
        sess = ph.setProxy(s, plist[i])
        r = sess.get(link)
    else:
        r = s.get(link)
    page = r.content
    soup = BeautifulSoup(page, "html.parser")
    matches = []
    if ch.getSite() == 5:
        # Available
        match1 = soup.body.findAll(text='The specified profile could not be found.')
        # Taken
        match2 = soup.body.findAll(text='This profile is private.')
        match3 = soup.find('div', attrs={'class': 'profile_header'})
        
        matches = [match1, match2, match3]
    elif ch.getSite() == 6:
        # Available
        match1 = soup.body.findAll(text='No group could be retrieved for the given URL.')
        # Taken
        match2 = soup.body.findAll(text='Request To Join')
        match3 = soup.find('div', attrs={'class': 'grouppage_header'})

        matches = [match1, match2, match3]
    else:
        print("Wrong site!")

    with print_lock:
        log_result(r, word, link, matches=matches)
            

def threader():
    while True:
        item = q.get()
        parseJob(item)
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
