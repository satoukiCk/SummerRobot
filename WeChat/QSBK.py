# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
import sys

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

class QSBK:
    def spider(self,page):
        url = 'https://www.qiushibaike.com/text/page/' + str(page)
        response = requests.get(url).content.decode('utf8')
        soup = BeautifulSoup(response, 'html.parser')
        jokes = soup.find_all('div', class_="article block untagged mb15")
        return jokes

    def get_joke(self):
        jokes = self.spider(random.randint(1,5))
        result = []
        for i in range(0, len(jokes)):
            joke = jokes[i].find('div', class_='content').text.strip()
            if '查看全文' not in joke:
                result.append(joke)
        num = random.randint(0,len(result)-1)
        return result[num]