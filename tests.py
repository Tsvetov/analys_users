# -*-coding: utf-8

# std
import random

# django
from django.test import TestCase
from django.test import Client
from django.db import IntegrityError
from django.utils import timezone

# models
from analys_users.models import UserIp


def test_generate_data(n=1):
    def __func_data():
        r_ = random.randint
        ip = '{num_0}.{num_1}.{num_2}.{num_3}'.format(
            num_0=r_(0, 255),
            num_1=r_(0, 255),
            num_2=r_(0, 255),
            num_3=r_(0, 255)
        )
        user_id = random.randint(0, 100000000)
        return user_id, ip
    for i in xrange(n):
        user_id, ip = __func_data()
        try:
            UserIp(
                ip_address=ip,
                user_id=user_id,
                date=timezone.now()
            ).save()
        except IntegrityError:
            pass


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