# -*- coding: utf-8 -*-

# std
from itertools import imap

# models
from analys_users.models import UserIP


class Message(object):
    """Класс где храняться в виде атрибутов сообщения"""
    # равенство идентификаторов
    equality = 'User_id_1 == user_id_2'

    # нет общих ip
    not_general_ip = 'No common ip'

    # нет общих подсетей
    not_general_network = 'Same IP within the network'

    # сообщение, когда пользователи взаимосвязаны
    ok_message = 'Users are interrelated'

    # в базе нет такого пользователя
    not_exist = 'Does not exist: {}'


def _get_user_id(user_id):
        """
            Вспомогательная функция для нахождения в базе записи, если ее нет,
            возвращаем False, message

            @param user_id: идентификатор пользователя
            @return: int

            @return: результат, сообщение or объект UserIP
            @rtype: tuple
        """
        try:
            return True, UserIP.objects.get(user_id=user_id)
        except UserIP.DoesNotExist:
            return False, Message.not_exist.format(user_id)


def check_users(user_id_1, user_id_2):
    """
        Метод для проверки связи пользователей.

        @param user_id_1: идентификатор первого пользователя
        @type: int

        @param user_id_2: идентификатор второго пользователя
        @type: int

        @return: результат, сообщение
        @rtype: tuple
    """

    # проверка на равенство id, если это так возвращаем True с комментариями
    if user_id_1 == user_id_2:
        return True, Message.equality

    # получение объектов бд, для этих id. Обработка случая когда
    # пользователей с такими id не существует.
    res_1, obj_1 = _get_user_id(user_id_1)
    res_2, obj_2 = _get_user_id(user_id_2)

    errors = []
    if not res_1:
        errors.append(obj_1)

    if not res_2:
        errors.append(obj_2)

    if errors:
        return False, ' || '.join(errors)

    # для начала проверяем по полю users
    if obj_2 in obj_1.users.all():
        # если это так, то никаких дополнительных проверок
        # и записей не требуется
        return True, Message.ok_message

    intersections = set(obj_1.ips) & set(obj_2.ips)

    # проверяем есть ли общие ip
    if len(intersections) <= 1:
        return False, Message.not_general_ip

    # проверяем из разной ли подсети эти ip
    intersections_network = set(
        imap(lambda ip: '.'.join((ip.split('.')[:3])), intersections)
    )
    if len(intersections_network) <= 1:
        return False, Message.not_general_network

    # записываем на будущее в поле users эту связь
    obj_1.users.add(obj_2)

    return True, Message.ok_message
