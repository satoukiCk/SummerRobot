# -*- coding:utf-8 -*-
import requests
import json
import random
import hashlib

KEY = ''
APPID = ''
API = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

class translation():
    def __init__(self,src, fromlang, tolang):
        self.src = src
        self.fromlang = fromlang
        self.tolang = tolang

    def trans(self):
        salt = random.randint(32768,65535)
        sign = APPID+self.src+str(salt)+KEY
        m1 = hashlib.md5()
        m1.update(sign)
        sign = m1.hexdigest()

        paras = {
            'q':self.src,
            'from':self.fromlang,
            'to':self.tolang,
            'appid':APPID,
            'salt':salt,
            'sign':sign
        }

        result = requests.get(API,params=paras,timeout=50)
        tdata = json.loads(result.text)
        res_msg = ''
        src = tdata['trans_result'][0]['src']
        dst = tdata['trans_result'][0]['dst']
        res_msg += '源语言: %s\n翻译结果: %s' % (src.encode('utf8'), dst.encode('utf8'))
        return res_msg
