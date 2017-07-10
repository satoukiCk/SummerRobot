# -*- coding:utf-8 -*-
import requests
import json

API = 'https://api.seniverse.com/v3/weather/daily.json'
UNIT = 'c'
LANGUAGE = 'zh-Hans'
KEY = ''
UID = ''


class weather():
    def __init__(self,city):
        self.city = city


    def get_weather(self):
        params={
            'key': KEY,
            'location': self.city,
            'language': LANGUAGE,
            'unit': UNIT,
        }
        result = requests.get(API,params,timeout=100)
        res_msg = '【 %s 】\n' % self.city

        '''
        if result.status_code == 200:
            wdata = json.loads(result.text)
            info = wdata['results'][0]
            res = ''
            weather_now = info['now']['text']
            temperature = info['now']['temperature']
            location = info['location']['name']
            res += '【%s】\n今天天气:%s\n温度:%s' % (
            location.encode('utf8'), weather_now.encode('utf8'), temperature.encode('utf8'))
        '''

        if result.status_code == 200:
            wdata = json.loads(result.text)
            info = wdata['results'][0]['daily']
            for day in info:
                date = day['date']
                day_weather = day['text_day']
                night_weather = day['text_night']
                high_temperature = day['high']
                low_temperature = day['low']
                wind_direction = day['wind_direction']
                wind_speed = day['wind_speed']
                res_msg += '日期: %s\n白天: %s\n夜晚: %s\n温度: %s~%s°C\n风向: %s\n风速: %skm/h\n\n'\
                           % (date.encode('utf8'), day_weather.encode('utf8'), night_weather.encode('utf8'),
                          low_temperature.encode('utf8'), high_temperature.encode('utf8'), wind_direction.encode('utf8'), wind_speed.encode('utf8'))

        else:
            res_msg = '没有您要查找的城市天气,请输入中国城市。'

        return res_msg
