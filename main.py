import time
from bs4 import BeautifulSoup
import lxml
from config import FRIDAY_GROUP_LINK
import requests


def handler_friday():
    current_wday = time.localtime().tm_wday + 1
    if current_wday == 5:
        return True


def get_last_friday_pic(link):
    res = requests.get(link).text
    soup = BeautifulSoup(res, "lxml")
    body = soup.select("div.wi_body")
    disc = body[0].select("div.pi_text")[0].text
    pic_src = body[0].select("a.MediaGrid__interactive")[0].attrs["data-src_big"]
    return [disc, pic_src]


if __name__ == '__main__':
    handler_friday()
    get_last_friday_pic(FRIDAY_GROUP_LINK)
