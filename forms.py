# -*-coding: utf-8 -*-

# django
from django import forms
from django.core.exceptions import ValidationError


def validate_non_negative(value):
    """
        Валидатор для проверки идентификатора на неотрицательность
    """
    if value < 0:
        raise ValidationError(u'%s is not an non-negative number' % value)


class UsersForm(forms.Form):
    id_user_1 = forms.IntegerField(validators=[validate_non_negative])
    id_user_2 = forms.IntegerField(validators=[validate_non_negative])
