# -*- coding:utf-8 -*-
from .models import feedback
import time

def add_feedback(user_id,content):
    fbtime = time.strftime('%Y-%m-%d %H:%M',time.localtime())
    obj = feedback(user=user_id,time=fbtime,fk_content=content)
    obj.save()
    if obj.id is None:
        return "error"
    else:
        return "已收到您的反馈"