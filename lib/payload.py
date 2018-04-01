from lib.configure import getSite as SITE
import string
import random

def generate_pw(size=16, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

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