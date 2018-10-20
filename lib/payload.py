import string
import random

from lib.ConfigHelper import ConfigHelper

ch = ConfigHelper()

def generate_pw(size=16, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def ready_payload(word):
    if ch.getSite() == 4:
        return {
            "email":"no-reply@crocbuzzstudios.com",
            "username": word,
            "password": generate_pw(),
            "first_name": word
        }
    else:
        print("Wrong site!")
        exit()