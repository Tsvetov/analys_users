# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import ArrayField


class UserIp(models.Model):
    """
        Модель с исходными данными.
    """
    class Meta:
        unique_together = ('user_id', 'ip_address')

    user_id = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    date = models.DateTimeField()


class UserSubNetwork(models.Model):
    """
        Модель, которая неявным образом сохраняет связи user-user.
        Эта модель заполняется триггрером
    """
    user_id = models.IntegerField(unique=True, db_index=True, primary_key=True)
    sub_networks = ArrayField(models.CharField(max_length=11))