import configparser
import os
import re

# Regex Patterns
PLACEHOLDER = r"%%(name|word)%%"
URLPATT = r"(^https?:\/\/[-.a-zA-Z0-9]+)"
DOMAIN = r"(?:https:\/\/)?(?:\w+\.)?(\w+)\.\w+\/?"

config = configparser.ConfigParser()
config.read('config.ini')

class ConfigHelper:

    def getSite(self):
        return config.getint('site', 'siteNum', fallback=5,)


    def getCustomUrl(self):
        url = config.get('site', 'customSite')
        if re.match(PLACEHOLDER, url):
            return url


    def enableProxy(self):
        return config.getboolean('proxy', 'enableProxy', fallback=False)


    def proxyFiltering(self):
        return config.getboolean('proxy', 'proxyFiltering', fallback=False)


    def getProxies(self, filename_only=False):
        if filename_only is True:
            return config.get('proxy', 'proxyList')
        proxies = []
        path = os.path.join("proxy_lists", config.get('proxy', 'proxyList'))
        if path is not None:
            fx = open(path, 'r')
            proxies = fx.read().split('\n')
            fx.close()
            return proxies
        else:
            if not self.enableProxy():
                print("Proxy support is disabled. Please enable it in the config.")
                exit()
            elif proxies is None:
                print("Specified proxy list is empty. Please add some proxies.")
                exit()
            else:
                print("Unknown error.")
                exit()

    def getWords(self):
        words = []
        path = os.path.join("word_lists", config.get('lists', 'wordList'))
        if path is not None:
            fx = open(path, 'r')
            words = fx.read().split('\n')
            fx.close()
            return words
        else:
            print("Word list not found.\n[DEBUG] %s" % path)


    def getOutputList(self):
        return config.get('lists', 'output', fallback="AVAILABLE.txt")


    def numThreads(self):
        return config.getint('multithreading', 'threadCount')