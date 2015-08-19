# -*-coding: utf-8

# std
import random

# django
from django.test import TestCase
from django.test import Client
from django.db import IntegrityError
from django.utils import timezone

# models
from analys_users.models import IPTable
from analys_users.models import UserIP

# utils
import analys_users.utils as ut


def test_generate_data(n=1):
    """
        Для массовой генерации случайных пар id_user-ip
        @param n: коллсичетсво пар
        @type: int

        @return: None
    """
    def __func_data():
        r_ = random.randint
        ip = '{num_0}.{num_1}.{num_2}.{num_3}'.format(
            num_0=r_(0, 255),
            num_1=r_(0, 255),
            num_2=r_(0, 255),
            num_3=r_(0, 255)
        )
        user_id = random.randint(0, 10000000)
        return user_id, ip
    for i in xrange(n):
        user_id, ip = __func_data()
        try:
            IPTable(
                ip_address=ip,
                user_id=user_id,
                date=timezone.now()
            ).save()
        except IntegrityError:
            pass


def gener_id_ip(user_id, *ips):
    """
        Для генерации заданных пар user_id-ip

        @param id: Идентификатор пользователя
        @type: int

        @param ip: список ip адресов
        @type: string

    @return: None
    """
    for ip in ips:
        try:

            IPTable(
                ip_address=ip,
                user_id=user_id,
                date=timezone.now()
            ).save()
        except IntegrityError:
            return False

    return True


def delete_tables(*args):
    """
        Удаление данных из таблиц

        @param args: список таблиц
        @type: объекты models
    """
    for i in args:
        i.objects.all().delete()


class TestSmoke(TestCase):
    def test_get_user_check(self):
        client = Client()
        response = client.get('/users_check/')
        self.assertEqual(response.status_code, 200)

    def test_post_user_check(self):
        client = Client()
        response = client.post(
            '/users_check/', {'id_user_1': 123, 'id_user_2': 3}
        )
        self.assertEqual(response.status_code, 302)

    def test_post_user_check_result_false(self):
        client = Client()
        client.post(
            '/users_check/', {'id_user_1': 123, 'id_user_2': 3}
        )
        self.assertEqual('res' in client._session().keys(), True)
        self.assertEqual(False in client._session().values(), True)


class TestCheckUser(TestCase):
    def setUp(self):
        self.user_1 = 1
        self.user_2 = 2

    def test_equality_ids(self):
        """OK.id пользователей равны"""
        gener_id_ip(self.user_1, '1.2.3.4')
        res, message = ut.check_users(self.user_1, self.user_1)
        delete_tables(IPTable, UserIP)
        self.assertEqual(res, True)
        self.assertEqual(message, ut.Message.equality)

    def test_2_general_ip(self):
        """
            OK.Есть 2 ОДИНАКОВЫХ ip адреса из разных подсетей
            напрмер: user_1: 1.2.3.4, 1.2.5.1 --- user_2: 1.2.3.4, 1.2.5.1
        """
        ips = ('1.2.3.4', '8.2.3.1')
        gener_id_ip(self.user_1, *ips)
        gener_id_ip(self.user_2, *ips)

        res, message = ut.check_users(self.user_1, self.user_2)

        delete_tables(IPTable, UserIP)
        self.assertEqual(res, True)
        self.assertEqual(message, ut.Message.ok_message)

    def test_more_general_ip(self):
        """
            OK. Есть более 2 ОДИНАКОВЫХ адреса из разных подсетей
            напрмер: user_1: 1.2.3.4, 1.2.5.1, 12.1.3.4 ---
            user_2: 1.2.3.4, 1.2.5.1, 12.1.3.4
        """
        ips = ('1.2.3.4', '1.2.5.1', '1.3.5.1')
        gener_id_ip(self.user_1, *ips)
        gener_id_ip(self.user_2, *ips)

        res, message = ut.check_users(self.user_1, self.user_2)

        delete_tables(IPTable, UserIP)
        self.assertEqual(res, True)
        self.assertEqual(message, ut.Message.ok_message)

    def test_1_general_ip(self):
        """
            NOT. Есть 1 ОДИНАКОВЫЙ ip адрес
            напрмер: user_1: 1.2.3.4 --- user_2: 1.2.3.4
        """
        ips = ('1.2.3.4',)
        gener_id_ip(self.user_1, *ips)
        gener_id_ip(self.user_2, *ips)

        res, message = ut.check_users(self.user_1, self.user_2)

        delete_tables(IPTable, UserIP)
        self.assertEqual(res, False)
        self.assertEqual(message, ut.Message.not_general_ip)

    def test_2_general_not_ip_and_general_network(self):
        """
            NOT. Есть 2 неодинаковых ip адреса из одной подсети
            напрмер: user_1: 1.2.3.88, 1.2.5.88 --- user_2: 1.2.3.89, 1.2.5.89
        """
        ips_1 = ('1.2.3.4', '1.2.4.7')
        ips_2 = ('1.2.3.5', '1.2.4.78')
        gener_id_ip(self.user_1, *ips_1)
        gener_id_ip(self.user_2, *ips_2)

        res, message = ut.check_users(self.user_1, self.user_2)

        delete_tables(IPTable, UserIP)
        self.assertEqual(res, False)
        self.assertEqual(message, ut.Message.not_general_ip)

    def test_general_not_ip(self):
        """
            NOT. NOT. Нет общих ip адресов
        """
        ips_1 = ('1.88.3.4', '1.2.4.7')
        ips_2 = ('1.2.124.5', '12.2.4.78')
        gener_id_ip(self.user_1, *ips_1)
        gener_id_ip(self.user_2, *ips_2)

        res, message = ut.check_users(self.user_1, self.user_2)

        delete_tables(IPTable, UserIP)
        self.assertEqual(res, False)
        self.assertEqual(message, ut.Message.not_general_ip)

    def test_id_not_exist_user(self):
        """
            NOT. id пользователя нет в базе
        """
        ips = ('1.88.3.4', '1.2.4.7')
        gener_id_ip(self.user_1, *ips)

        res, message = ut.check_users(self.user_1, self.user_2)

        delete_tables(IPTable, UserIP)
        self.assertEqual(res, False)
        self.assertEqual(message, ut.Message.not_exist.format(self.user_2))

    def test_id_not_exist_users(self):
        """
            NOT. Случай, когда обоих пользователй нет в базе
        """

        res, message = ut.check_users(self.user_1, self.user_2)
        message_total = ' || '.join((
            ut.Message.not_exist.format(self.user_1),
            ut.Message.not_exist.format(self.user_2)
        ))
        self.assertEqual(res, False)
        self.assertEqual(
            message,
            message_total
        )

    def test_2_general_ip_1_network(self):
        """
            NOT. Есть 2 одинаковых ip адреса, но они из одной подсети
            (например user_1: 1.2.3.4, 1.2.3.1 --- user_2: 1.2.3.4, 1.2.3.1)).
        """
        ips = ('1.2.3.4', '1.2.3.1')
        gener_id_ip(self.user_1, *ips)
        gener_id_ip(self.user_2, *ips)
        res, message = ut.check_users(self.user_1, self.user_2)

        delete_tables(IPTable, UserIP)
        self.assertEqual(res, False)
        self.assertEqual(message, ut.Message.not_general_network)

    def test_more_general_ip_1_network(self):
        """
            NOT. Есть более 2 одинаковых ip адреса, но они из одной подсети
            напрмер: user_1: 1.2.3.1, 1.2.3.2, 1.2.3.3 ---
            user_2: 1.2.3.1, 1.2.3.2, 1.2.3.3)
        """
        ips = ('1.2.3.1', '1.2.3.2', '1.2.3.3')
        gener_id_ip(self.user_1, *ips)
        gener_id_ip(self.user_2, *ips)
        res, message = ut.check_users(self.user_1, self.user_2)

        delete_tables(IPTable, UserIP)
        self.assertEqual(res, False)
        self.assertEqual(message, ut.Message.not_general_network)

    def test_check_user_user(self):
        """Проверка записи связи users-users"""

        ips = ('1.2.3.4', '8.2.3.1')
        gener_id_ip(self.user_1, *ips)
        gener_id_ip(self.user_2, *ips)

        res, message = ut.check_users(self.user_1, self.user_2)

        obj = UserIP.objects.get(pk=self.user_1)

        self.assertEqual(res, True)
        self.assertEqual(self.user_2 in [i.pk for i in obj.users.all()], True)

        delete_tables(IPTable, UserIP)
