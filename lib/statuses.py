import threading
from lib.configure import getOutputList as OUTPUT

def taken(word, service, error=None):
    if error != None:
        msg = "%s %s is TAKEN on %s because %s" % (threading.current_thread().name, word, service, error)
        print(msg)
    else:
        msg = "%s %s is TAKEN on %s." % (threading.current_thread().name, word, service)
        print(msg)

def available(word, service, link):
    msg = "%s %s is AVAILABLE on %s." % (threading.current_thread().name, word, service)
    print(msg)
    fx = open(OUTPUT(), 'a')
    fx.write(link + "\n")
    fx.close()

def manual(response, word, service):
    msg = "%s The username %s requires manual verification on %s (%d)." % (threading.current_thread().name, word, service, response.status_code)
    print(msg)
    