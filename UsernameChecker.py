from configparser import SafeConfigParser
import requests
import json
import re
from termcolor import colored
from bs4 import BeautifulSoup

# Global Variables
sites = []
pattern = "(%[w][o][r][d]%)"
steam_url_pattern = "^https?:\/\/w?w?w?.?(steamcommunity.com\/id\/)"
beam_url_pattern = "^https?:\/\/w?w?w?.?(beam.pro\/api\/v1\/channels\/)"

# Reads configuration file
parser = SafeConfigParser()
parser.read('config.ini')
url = parser.get('config', 'siteToSearch')
list = parser.get('config', 'wordList')
text = parser.get('config', 'textToFind')

def replaceVar():
    # Reads word list from file and adds each name to array words[]
    file = open(list, 'r')
    words = file.read().split('\n')
    file.close()

    # Finds and replaces matches of the name variable with the actual word to insert in URL
    numWords = words.__len__()
    for i in range(numWords):
        x = re.sub(pattern, words[i], url)
        sites.append(x)

def parsePages(links):
    numLinks = links.__len__()
    for l in range(numLinks):
        r = requests.get(links[l])
        if (r.status_code == requests.codes.ok):
            print(links[l] + " is " + colored('TAKEN', 'red', attrs=['bold']))
        else:
            print(links[l] + " is " + colored('AVAILABLE', 'green', attrs=['bold']))
            file = open('available.txt', 'a')
            file.write(links[l] + "\n")
            file.close()

def checkSteamID(links):
    numLinks = links.__len__()
    for l in range(numLinks):
        page = requests.get(links[l])
        r = page.content
        soup = BeautifulSoup(r, "html.parser")
        matches = soup.find_all("h3")
        pp = soup.find('div', attrs={'class': 'profile_private_info'})
        for match in matches:
            if not match:
                print(links[l] + " is " + colored('TAKEN', 'red', attrs=['bold']))
            elif pp:
                print(links[l] + " is " + colored('TAKEN', 'red', attrs=['bold']))
            else:
                print(links[l] + " is " + colored('AVAILABLE', 'green', attrs=['bold']))
                file = open('available.txt', 'a')
                file.write(links[l] + "\n")
                file.close()

def checkBeam(links):
    numLinks = links.__len__()
    for l in range(numLinks):
        response = requests.get(links[l])
        json_data = json.loads(response.text)
        if 'statusCode' in json_data:
            print(links[l] + " is " + colored('AVAILABLE', 'green', attrs=['bold']))
            file = open('available.txt', 'a')
            file.write(links[l] + "\n")
            file.close()
        else:
            print(links[l] + " is " + colored('TAKEN', 'red', attrs=['bold']))

def main():
    replaceVar()
    if re.match(steam_url_pattern, url):
        checkSteamID(sites)
    elif re.match(beam_url_pattern, url):
        checkBeam(sites)
    else:
        parsePages(sites)

main()

