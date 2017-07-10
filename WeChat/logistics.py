# -*- coding:utf-8 -*-
import requests
import json
import hashlib
import base64

APP_KEY = ''
APP_ID = ''
API = 'http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx'
header = {
        "Accept": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept-Encoding": "utf-8"
    }


class logistics():
    @staticmethod
    def encrypt(key, rd):
        m = hashlib.md5()
        m.update(rd + key)
        md5_str = m.hexdigest()
        b64_str = base64.urlsafe_b64encode(md5_str)
        return b64_str

    def get_shipper(self, logistic_code):
        rd = {"LogisticCode": logistic_code}
        rd_json = json.dumps(rd)
        sign = self.encrypt(APP_KEY, rd_json)
        param = {
            'RequestData': rd_json,
            'EBusinessID': APP_ID,
            'RequestType': '2002',
            'DataSign': sign,
            'DataType': '2'
        }
        result = requests.get(API, params=param, timeout=200, headers=header)
        kdata = json.loads(result.text)
        return kdata

    def get_traces(self, shipper_code, logistic_code):
        rd = {'ShipperCode': shipper_code, 'LogisticCode': logistic_code}
        rd_json = json.dumps(rd)
        sign = self.encrypt(APP_KEY, rd_json)
        param = {
            'RequestData': rd_json,
            'EBusinessID': APP_ID,
            'RequestType': '1002',
            'DataSign': sign,
            'DataType': '2'
        }
        result = requests.get(API, params=param, timeout=200, headers=header)
        tdata = json.loads(result.text)
        return tdata

    def show_order(self, lc):
        kdata = self.get_shipper(lc)
        if not any(kdata['Shippers']):
            return "没有查到相关快递信息,请尝试重新输入。"
        else:
            shipper_code = kdata['Shippers'][0]['ShipperCode']
            shipper_name = kdata['Shippers'][0]['ShipperName']

            tdata = self.get_traces(shipper_code, lc)
            msg = '物流编号: %s\n' % lc.encode('utf-8')
            msg += '快递公司: %s\n物流状态: ' % shipper_name.encode('utf-8')

            if tdata['State'] == '2':
                msg += '在途中\n'
            if tdata['State'] == '3':
                msg += '已签收\n'
            if tdata['State'] == '4':
                msg += '问题件\n'
            if tdata['State'] == '0':
                msg += '此单无物流状态\n'

            msg += '物流信息:\n'
            if not any(tdata['Traces']):
                msg += '暂无物流信息\n'

            traces = tdata['Traces']
            for t in range(0,len(traces)-1):
                acceptime = traces[t]['AcceptTime']
                acceptstation = traces[t]['AcceptStation']
                msg += '【 %s 】\n%s\n\n' % (acceptime.encode('utf-8'), acceptstation.encode('utf-8'))
            acceptime = traces[len(traces)-1]['AcceptTime']
            acceptstation = traces[len(traces)-1]['AcceptStation']
            msg += '【 %s 】\n%s' % (acceptime.encode('utf-8'), acceptstation.encode('utf-8'))

            return msg
