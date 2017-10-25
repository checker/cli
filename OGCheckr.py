# Python Standard Modules
import sys
import os

from lib.configure import getSite as SITE

def main():
    if (SITE() == 5) or (SITE() == 6): # Steam
        import lib.parse
    else:
        import lib.get

if __name__ == "__main__":
    main()
