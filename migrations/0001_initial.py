# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('ip_address', models.GenericIPAddressField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserIP',
            fields=[
                ('user_id', models.IntegerField(unique=True, serialize=False, primary_key=True)),
                ('ips', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), size=None)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='iptable',
            unique_together=set([('user_id', 'ip_address')]),
        ),
    ]
