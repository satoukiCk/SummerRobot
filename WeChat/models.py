# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class feedback(models.Model):
    user = models.TextField("OPENID",max_length=50)
    time = models.TextField("反馈时间",max_length=50)
    fk_content = models.TextField("反馈内容",max_length=50)

    def __str__(self):
        return self.fk_content

