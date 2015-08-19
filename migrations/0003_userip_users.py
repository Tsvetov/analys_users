# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analys_users', '0002_auto_20150818_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='userip',
            name='users',
            field=models.ManyToManyField(related_name='users_rel_+', to='analys_users.UserIP'),
        ),
    ]
