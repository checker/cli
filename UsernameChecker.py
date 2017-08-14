# Python Standard Modules
import sys
import os
import json
import re
import string
import random
# PyPi Modules
import configparser
import requests
from termcolor import colored
from bs4 import BeautifulSoup

# Global Variables
WORDS = []
SITES = []

# CLI Arguments
WORD_LIST = ""
OUTPUT = "AVAILABLE.txt"

# Regex Patterns
PLACEHOLDER = r"(%word%)"
URLPATT = r"(^https?:\/\/[-.a-zA-Z0-9]+)"
DOMAIN = r"\.([a-zA-Z0-9]+)\."

# Reads configuration file
config = configparser.ConfigParser()
config.read('config.ini')

SITE = config['site']['siteNum']
URL = config['site']['customSite']
PROXY = config['lists']['proxyList']

if URL != "":
    URL = re.match(URLPATT, URL).group(0)
else:
    URL = "http://google.com/"

# Site URLs
URLS = {
    1:URL,
    2:"https://api.mojang.com/users/profiles/minecraft/%word%",
    3:"https://api.twitter.com/i/users/username_available.json?username=%word%",
    4:"https://www.instagram.com/accounts/web_create_ajax/attempt/",
    5:"https://steamcommunity.com/id/%word%",
    6:"https://steamcommunity.com/groups/%word%",
    7:"https://soundcloud.com/%word%",
    8:"https://twitch.tv/%word%",
    9:"https://mixer.com/api/v1/channels/%word%",
    10:"https://github.com/%word%",
    11:"https://about.me/%word%"
}

def generate_pw(size=16, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def replace(word):
    # Finds and replaces matches of the name variable with the actual word to insert in URL
    if SITE != 4: # if not Instagram
        x = re.sub(PLACEHOLDER, word, URLS[SITE])
        return x
    else:
        print("instagram")

def taken(word, service, error=None):
    if error != None:
        print(word + " is " + colored('TAKEN', 'red', attrs=['bold']) + " on " + service + " because " + error)
    else:
        print(word + " is " + colored('TAKEN', 'red', attrs=['bold']) + " on " + service)

def available(word, service, link):
    print(word + " is " + colored('AVAILABLE', 'green', attrs=['bold']) + " on " + service)
    fx = open(OUTPUT, 'a')
    fx.write(link + "\n")
    fx.close()

def log_result(response, word, link=None, element=None, matches=None):
    service = re.match(DOMAIN, link).group(1)
    if (not matches) or (element != None):
        taken(word, service)
    elif response.status_code == 200:
        if SITE == 3: # Twitter
            obj = json.loads(response.json())
            if obj['valid'] == True:
                available(word, service, link)
            else:
                taken(word, service, obj['msg'])
        elif SITE == 4: #Instagram
            obj = json.loads(response.json())
            if obj['dryrun_passed'] == True:
                available(word, service, link)
            else:
                taken(word, service, obj['errors']['username']['code'])
        elif SITE == 2: #Minecraft
            obj = json.loads(response.json())
            if 'name' in obj:
                taken(word, service)
                if 'errorMessage' in obj:
                    print(obj['errorMessage'])
        elif SITE == 9: # Mixer
            obj = json.loads(response.json())
            if 'statusCode' in obj:
                available(word, service, link)
            else:
                taken(word, service)
        else:
            available(word, service, link)
    elif (SITE == 2) and (response.status_code == 204):
        available(word, service, link)
    else:
        print("The username " + word + " requires manual verification on " + service)

def get_cookie():
    r = requests.get(URLS[SITE])
    return r.cookies

def ready_payload(word):
    if SITE == 4:
        return {
            "email":"no-reply@crocbuzzstudios.com",
            "username": word,
            "password": generate_pw(),
            "first_name": "Croc"
        }
    else:
        print("Wrong site!")
        exit()

def prepare_headers(cookie):
    if SITE == 4:
        return {
            "referer":"https://www.instagram.com",
            "x-crsftoken": cookie
        }
    else:
        print("Wrong site!")
        exit()

def send_get():
    numWords = WORDS.__len__()
    for w in range(numWords):
        link = replace(w)
        r = requests.get(link)
        log_result(r, w, link=link)

def parse_page():
    numWords = WORDS.__len__()
    for w in range(numWords):
        link = replace(w)
        r = requests.get(link)
        page = r.content
        soup = BeautifulSoup(page, "html.parser")
        matches = []
        elem = ""
        if SITE == 5:
            matches = soup.find_all("h3")
            elem = soup.find('div', attrs={'class': 'profile_private_info'})
        elif SITE == 6:
            matches = soup.find_all("h3")
            elem = soup.find('div', attrs={'class': 'error_ctn'})
        elif SITE == 8:
            matches = soup.find_all("h3")
            elem = soup.find('div', attrs={'id': 'player'})
        else:
            print("Wrong site!")
        log_result(r, w, link=link, element=elem, matches=matches)

def send_post():
    numWords = WORDS.__len__()
    cookie = get_cookie()
    header = prepare_headers(cookie['crsftoken'])
    for w in range(numWords):
        payload = ready_payload(w)
        r = requests.post(URLS[SITE], json=payload, headers=header)
        log_result(r, w)

def main():
    # Reads word list from file and adds each name to array words[]
    fx = open(WORD_LIST, 'r')
    WORDS = fx.read().split('\n')
    fx.close()
    
    if (SITE == 5) or (SITE == 6) or (SITE == 8): # Steam and Twitch
        parse_page()
    elif SITE == 4: # Instagram
        send_post()
    else:
        send_get()

# Checking command line arguments if any
if len(sys.argv) != 6:
    print('Invalid usage.\n Correct arguments:\n -l, -o, site number \n\nExample usage:\n python namechecker.py -l list.txt -o output.txt 2')
    ans = raw_input("You have not specified any additional command line arugments.\nWould you like to run the script based on values in the config.ini? (y|N)")
    if ans == "y":
        WORD_LIST = config['lists']['wordList']
        OUTPUT = config['lists']['output']
        main()
    elif ans == "N":
        confirm = raw_input("Continue executing script? (y|N)")
        if confirm == "y":
            print("_________________________________\n| SERVICE     |  VALUE TO ENTER |\n_________________________________\n| CUSTOM      |       1         |\n| MINECRAFT   |       2         |\n| TWITTER     |       3         |\n| INSTAGRAM   |       4         |\n| STEAM ID    |       5         |\n| STEAM GROUP |       6         |\n| SOUNDCLOUD  |       7         |\n| TWITCH      |       8         |\n| MIXER       |       9         |\n| GITHUB      |       10        |\n| ABOUT.ME    |       11        |\n_________________________________\nQuit? (y/N)\n")
            SITE = raw_input("Enter the number from the table above with the site you want to check...")
            
            if SITE.isdigit():
                WORD_LIST = raw_input("Enter the local path to the word wordList you would like to use...")
                main()
            elif SITE == "y":
                print("Have a nice day!\n")
                exit()
            elif SITE == "N":
                SITE = raw_input("Enter the number from the table above with the site you want to check...")
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