# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import ArrayField


class IPTable(models.Model):
    """
        Модель с исходными данными.
    """
    class Meta:
        unique_together = ('user_id', 'ip_address')

    user_id = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    date = models.DateTimeField()


class UserIP(models.Model):
    """
        Модель, которая неявным образом сохраняет связи user-user.
        Эта модель заполняется триггрером
    """
    user_id = models.IntegerField(unique=True, primary_key=True)
    ips = ArrayField(models.CharField(max_length=15))

    # рекурсивная связь многи-ко-многим для записей уже просчитаных связей
    # user-user
    users = models.ManyToManyField('self')
