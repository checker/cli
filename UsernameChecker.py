# Python Standard Modules
import sys
import os
import re
import string
import random
# PyPi Modules
import configparser
import requests
from termcolor import colored
from bs4 import BeautifulSoup

# CLI Arguments
WORD_LIST = "word_lists/WORD-LIST-1"
OUTPUT = "AVAILABLE.txt"

# Regex Patterns
URLPATT = r"(^https?:\/\/[-.a-zA-Z0-9]+)"
DOMAIN = r"https?:\/\/(\w*)(?(1)\.|(?(1)\w*))"

# Reads configuration file
config = configparser.ConfigParser()
config.read('config.ini')

SITE = config['site']['siteNum']
URL = config['site']['customSite']
PROXY = config['proxy']['enableProxy']
PROTOCOL = config['proxy']['proxyProtocol']
PROXYLIST = config['proxy']['proxyList']


# Site URLs
URLS = {
    1:URL,
    2:"https://api.mojang.com/users/profiles/minecraft/%s",
    3:"https://api.twitter.com/i/users/username_available.json?username=%s",
    4:"https://instagram.com/accounts/web_create_ajax/attempt/",
    5:"https://steamcommunity.com/id/%s",
    6:"https://steamcommunity.com/groups/%s",
    7:"https://soundcloud.com/%s",
    8:"https://passport.twitch.tv/usernames/%s",
    9:"https://mixer.com/api/v1/channels/%s",
    10:"https://github.com/%s",
    11:"https://about.me/%s",
    12:"https://youtube.com/%s"
}

# Proxy List
proxyDict = {}

s = requests.Session()

def generate_pw(size=16, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def replace(word):
    # Finds and replaces matches of the name variable with the actual word to insert in URL
    if int(SITE) != 4: # if not Instagram
        return URLS[int(SITE)] % word
    else:
        print("instagram")

def get_proxy():
    if PROXY and (PROXYLIST != []):
        fx = open(PROXYLIST, 'r')
        proxies = fx.read().split('\n')
        fx.close()

        i = random.randrange(0, proxies.__len__())
        return str(proxies[i])
    else:
        if not PROXY:
            print("Proxy support is disabled. Please enable it in the config.")
        elif PROXYLIST == []:
            print("No proxies available to use.")

def taken(word, service, error=None):
    if error != None:
        print(str(word) + " is " + colored('TAKEN', 'red', attrs=['bold']) + " on " + str(service) + " because " + str(error))
    else:
        print(str(word) + " is " + colored('TAKEN', 'red', attrs=['bold']) + " on " + str(service))

def available(word, service, link):
    print(str(word) + " is " + colored('AVAILABLE', 'green', attrs=['bold']) + " on " + str(service))
    fx = open(OUTPUT, 'a')
    fx.write(link + "\n")
    fx.close()

def manual(response, word, service):
    print("The username " + word + " requires manual verification on " + service + " (" + str(response.status_code) + ")")

def log_result(response, word, link, matches=None):
    service = re.search(DOMAIN, link).group(1)
    if matches != None:
        if matches[0] != []:
            available(word, service, link)
        elif matches[1]:
            taken(word, service)
        elif matches[2]:
            taken(word, service)
        else:
            manual(response, word, service)
        
    elif response.status_code == 200:
        if int(SITE) == 3: # Twitter
            obj = response.json()
            if obj['valid'] == True:
                available(word, service, link)
            else:
                err = obj['msg']
                taken(word, service, error=err)
        elif int(SITE) == 4: # Instagram
            obj = response.json()
            if obj['dryrun_passed'] == True:
                available(word, service, link)
            else:
                err = obj['errors']['username'][0]['code']
                taken(word, service, error=err)
        elif int(SITE) == 2: #Minecraft
            obj = response.json()
            if 'name' in obj:
                taken(word, service)
                if 'errorMessage' in obj:
                    print(obj['errorMessage'])
        elif int(SITE) == 9: # Mixer
            obj = response.json()
            if 'statusCode' in obj:
                available(word, service, link)
            else:
                taken(word, service)
        elif int(SITE) == 8: # Twitch
            taken(word, service)
        else:
            taken(word, service)
    elif response.status_code == 204:
        if int(SITE) == 2:
            available(word, service, link)
        elif int(SITE) == 8:
            available(word, service, link)
        else:
            manual(response, word, service)
    elif response.status_code == 404:
        available(word, service, link)
    else:
        manual(response, word, service)

def get_cookie():
    r = s.get(URLS[int(SITE)])
    return r.cookies

def ready_payload(word):
    if int(SITE) == 4:
        return {
            "email":"no-reply@crocbuzzstudios.com",
            "username": word,
            "password": generate_pw(),
            "first_name": word
        }
    else:
        print("Wrong site!")
        exit()

def prepare_headers(cookie):
    if int(SITE) == 4:
        return {
            "referer":"https://www.instagram.com",
            "x-csrftoken": cookie['csrftoken']
        }
    else:
        print("Wrong site!")
        exit()

def send_get(words):
    for w in range(words.__len__()):
        link = replace(words[w])
        if PROXY:
            proxyDict[PROTOCOL] = get_proxy()
            r = s.get(link, proxies=proxyDict)
        else:
            r = s.get(link)
        log_result(r, words[w], link)

def parse_page(words):
    for w in range(words.__len__()):
        link = replace(words[w])
        if PROXY:
            proxyDict[PROTOCOL] = get_proxy()
            r = s.get(link, proxies=proxyDict)
        else:
            r = s.get(link)
        page = r.content
        soup = BeautifulSoup(page, "html.parser")
        matches = []
        if int(SITE) == 5:
            # Available
            match1 = soup.body.findAll(text='The specified profile could not be found.')
            # Taken
            match2 = soup.body.findAll(text='This profile is private.')
            match3 = soup.find('div', attrs={'class': 'profile_header'})
            
            matches = [match1, match2, match3]
        elif int(SITE) == 6:
            # Available
            match1 = soup.body.findAll(text='No group could be retrieved for the given URL.')
            # Taken
            match2 = soup.body.findAll(text='Request To Join')
            match3 = soup.find('div', attrs={'class': 'grouppage_header'})

            matches = [match1, match2, match3]
        else:
            print("Wrong site!")
        log_result(r, words[w], link, matches=matches)

def send_post(words):
    cookie = get_cookie()
    header = prepare_headers(cookie)
    link = URLS[int(SITE)]
    for w in range(words.__len__()):
        payload = ready_payload(words[w])
        r = None
        if PROXY:
            proxyDict[PROTOCOL] = get_proxy()
            r = s.post(URLS[int(SITE)], data=payload, headers=header, cookies=cookie, proxies=proxyDict)
        else:
            r = s.post(URLS[int(SITE)], data=payload, headers=header, cookies=cookie)
        
        log_result(r, words[w], link)

def main():
    # Reads word list from file and adds each name to array words[]
    fx = open(WORD_LIST, 'r')
    words = fx.read().split('\n')
    fx.close()

    if (int(SITE) == 5) or (int(SITE) == 6): # Steam
        parse_page(words)
    elif int(SITE) == 4: # Instagram
        send_post(words)
    else:
        send_get(words)

# if __name__ == "__main__":
#     main()

# Checking command line arguments if any
if len(sys.argv) != 6:
    print('Invalid usage.\n Correct arguments:\n -l, -o, site number \n\nExample usage:\n python namechecker.py -l list.txt -o output.txt 2')
    ans = input("You have not specified any additional command line arugments.\nWould you like to run the script based on values in the config.ini? (y|N)")
    if ans == "y":
        WORD_LIST = config['lists']['wordList']
        OUTPUT = config['lists']['output']
        main()
    elif ans == "N":
        confirm = input("Continue executing script? (y|N)")
        if confirm == "y":
            print("_________________________________\n| SERVICE     |  VALUE TO ENTER |\n_________________________________\n| CUSTOM      |       1         |\n| TWITTER     |       3         |\n| INSTAGRAM   |       4         |\n| STEAM ID    |       5         |\n| STEAM GROUP |       6         |\n| SOUNDCLOUD  |       7         |\n| TWITCH      |       8         |\n| MIXER       |       9         |\n| GITHUB      |       10        |\n| ABOUT.ME    |       11        |\n| YOUTUBE     |       12        |\n_________________________________\nQuit? (y/N)\n")
            SITE = input("Enter the number from the table above with the site you want to check...")
            
            if SITE.isdigit():
                WORD_LIST = input("Enter the local path to the word wordList you would like to use...")
                main()
            elif int(SITE) == "y":
                print("Have a nice day!\n")
                exit()
            elif int(SITE) == "N":
                SITE = input("Enter the number from the table above with the site you want to check...")
            else:
                print("Sorry, I don\'t understand.")
                exit()
        elif confirm == "N":
            print("Have a nice day!\n")
            exit()
        else:
            print("Sorry, I don\'t understand.")
            exit()
    else:
        print("Sorry, I don\'t understand.")
        exit()
else:
    if sys.argv[1] != "-l":
        print('Unknown parameter. Use -l or -o')
    else:
        if sys.argv[3] != "-o":
            print('Unknown parameter. Use -l or -o')
        else:
            if os.path.isfile(os.path.join(os.path.dirname(sys.argv[0]), sys.argv[2])):
                WORD_LIST = sys.argv[2]
                OUTPUT = sys.argv[4]
                SITE = sys.argv[5]
                print('File exists. Running availability checker...')
                main()
            else:
                print('File: \'' + os.path.join(os.path.dirname(sys.argv[0]), sys.argv[2]) + 'doesn\'t exist.')