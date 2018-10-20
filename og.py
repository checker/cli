#!/usr/bin/env python3
# Python Standard Modules
import sys
import os

from lib.ConfigHelper import ConfigHelper
from lib.ProxyHelper import ProxyHelper

ch = ConfigHelper()
ph = ProxyHelper()

def main():
    if ch.enableProxy():
        if ch.proxyFiltering():
            ph.checkProxies()

    if (ch.getSite() == 5) or (ch.getSite() == 6): # Steam
        import lib.parse
    elif ch.getSite() == 4:
        import lib.post
    else:
        import lib.get

if __name__ == "__main__":
    main()
