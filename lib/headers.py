from lib.ConfigHelper import ConfigHelper

ch = ConfigHelper()

def prepare_headers(cookie):
    if ch.getSite() == 4:
        return {
            "referer":"https://www.instagram.com",
            "x-csrftoken": cookie['csrftoken']
        }
    else:
        print("Wrong site!")
        exit()