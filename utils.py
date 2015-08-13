# -*- coding: utf-8 -*-

# models
from analys_users.models import UserSubNetwork

__author__ = 'cpn'


def check_users(user_id_1, user_id_2):
    """
        Метод для проверки связи пользователей.

        @param user_id_1: идентификатор первого пользователя
        @type: int

        @param user_id_2: идентификатор второго пользователя
        @type: int

        @return: результат
        @rtype: bool
    """
    try:
        objs_1 = UserSubNetwork.objects.get(user_id=user_id_1)
        objs_2 = UserSubNetwork.objects.get(user_id=user_id_2)
    except UserSubNetwork.DoesNotExist:
        return False

    if len(set(objs_1.sub_networks) & set(objs_2.sub_networks)) > 1:
        return True
    else:
        return False

