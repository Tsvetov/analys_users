# -*-coding: utf-8 -*-

__author__ = 'cpn'

# django
from django import forms


class UsersForm(forms.Form):
    id_user_1 = forms.IntegerField()
    id_user_2 = forms.IntegerField()




