#!/usr/bin/env python3
# Python Standard Modules
import sys
import os
from lib.configure import getSite as SITE
from lib.configure import enableProxy as PROXY
from lib.configure import proxyFiltering as PFILTER
from lib.ProxyHelper import ProxyHelper

def main():
    if PROXY() == "True":
        if PFILTER() == "True":
            ProxyHelper().checkProxies()

    if (SITE() == 5) or (SITE() == 6): # Steam
        import lib.parse
    elif SITE() == 4:
        import lib.post
    else:
        import lib.get

if __name__ == "__main__":
    main()
