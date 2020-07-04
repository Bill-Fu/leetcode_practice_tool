import requests

from config import *
from enum import Enum


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class CrawlerLeetcode:
    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies
        self.client = requests.session()

    def get_problems_info(self):
        return self.client.get(self.url, cookies=self.cookies).json()


crawlerLeetcode = CrawlerLeetcode(URL_LEETCODE, COOKIES_LEETCODE)