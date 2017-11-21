import re
from lib.statuses import *
from lib.configure import getSite as SITE
from lib.configure import DOMAIN

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
        if SITE() == 3: # Twitter
            obj = response.json()
            if obj['valid'] == True:
                available(word, service, link)
            else:
                err = obj['msg']
                taken(word, service, error=err)
        elif SITE() == 4: # Instagram
            obj = response.json()
            if obj['dryrun_passed']:
                available(word, service, link)
            else:
                taken(word, service)
        elif SITE() == 2: #Minecraft
            obj = response.json()
            if 'name' in obj:
                taken(word, service)
                if 'errorMessage' in obj:
                    print(obj['errorMessage'])
        elif SITE() == 9: # Mixer
            obj = response.json()
            if 'statusCode' in obj:
                available(word, service, link)
            else:
                taken(word, service)
        elif SITE() == 8: # Twitch
            taken(word, service)
        else:
            taken(word, service)
    elif response.status_code == 204:
        if SITE() == 2:
            available(word, service, link)
        elif SITE() == 8:
            available(word, service, link)
        else:
            manual(response, word, service)
    elif response.status_code == 404:
        available(word, service, link)
    else:
        manual(response, word, service)