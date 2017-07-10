# -*- coding:utf-8 -*-
import requests
import json

API_KEY = ''
API = 'http://www.tuling123.com/openapi/api'


class TrRobot:
    def __init__(self,info):
        self.info = info


    def conversation(self):
        datas = {
            "key":API_KEY,
            "info":self.info,
            "userid":''
        }

        result = requests.post(API,data=datas)
        tdata = json.loads(result.text)
        return tdata