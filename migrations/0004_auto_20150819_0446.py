# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analys_users', '0003_userip_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userip',
            name='user_id',
            field=models.IntegerField(unique=True, serialize=False, primary_key=True, db_index=True),
        ),
    ]
