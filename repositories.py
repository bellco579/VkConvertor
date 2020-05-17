import random
import string

import requests


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def downloadPhoto(url):
    path = "photos/"+randomString() + ".png"
    photo = requests.get(url=url)
    file = open(path, "wb")
    file.write(photo.content)
    file.close()
    return path

if __name__ == '__main__':
    downloadPhoto('https://sun9-29.userapi.com/c855216/v855216959/21505f/VUDIInSpFL4.jpg')