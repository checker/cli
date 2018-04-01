import configparser

# Regex Patterns
PLACEHOLDER = r"%word%"
URLPATT = r"(^https?:\/\/[-.a-zA-Z0-9]+)"
DOMAIN = r"(?:https:\/\/)?(?:\w+\.)?(\w+)\.\w+\/?"

# Reads configuration file
config = configparser.ConfigParser()
config.read('config.ini')


def getSite():
    x = config['site']['siteNum']
    if x == "":
        print("A site must be specified in the config file or via CLI arguments.")
        exit()
    else:
        return int(x)

def getCustomUrl():
    x = config['site']['customSite']
    if x == "":
        print("A url must be specified in the config file for the customSite option. Ex: https://twitter.com/test")
        exit()
    else:
        return str(x)

def enableProxy():
    x = config['proxy']['enableProxy']
    if x == "":
        print("Either True or False must be specified for enableProxy in the config file.")
        exit()
    else:
        return x

def proxyFiltering():
    x = config['proxy']['proxyFiltering']
    if x == "":
        print("Either True or False must be specified for proxyFiltering in the config file.")
        exit()
    else:
        return x

def getProxyList():
    proxies = []
    path = "proxy_lists/" + config['proxy']['proxyList']
    if path is not None:
        fx = open(path, 'r')
        proxies = fx.read().split('\n')
        fx.close()
        return proxies
    else:
        if not enableProxy():
            print("Proxy support is disabled. Please enable it in the config.")
            exit()
        elif proxies is None:
            print("Specified proxy list is empty. Please add some proxies.")
            exit()
        else:
            print("Unkown error.")
            exit()

def getWordList():
    x = "word_lists/" + config['lists']['wordList']
    if x == "":
        print("Place just the filename of the list for wordList in the config file.\nAll word lists go in the word_lists directory.")
        exit()
    else:
        return str(x)


def getOutputList():
    x = config['lists']['output']
    if x == "":
        print("Enter the filename for the file you want the available names to be logged to.")
        exit()
    else:
        return str(x)


def numThreads():
    x = config['multithreading']['threadCount']
    if x == "":
        print("Enter the number of processor threads you want to use.")
        exit()
    else:
        return int(x)
