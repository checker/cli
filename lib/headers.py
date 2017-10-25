from lib.configure import getSite as SITE

def prepare_headers(cookie):
    if SITE() == 4:
        return {
            "referer":"https://www.instagram.com",
            "x-csrftoken": cookie['csrftoken']
        }
    else:
        print("Wrong site!")
        exit()