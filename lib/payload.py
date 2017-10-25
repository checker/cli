from lib.generate import *
from lib.configure import getSite as SITE

def ready_payload(word):
    if SITE() == 4:
        return {
            "email":"no-reply@crocbuzzstudios.com",
            "username": word,
            "password": generate_pw(),
            "first_name": word
        }
    else:
        print("Wrong site!")
        exit()