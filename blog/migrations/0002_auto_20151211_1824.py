# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-11 10:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='fromperson',
            field=models.CharField(default=datetime.datetime(2015, 12, 11, 10, 24, 4, 741691, tzinfo=utc), max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mail',
            name='subject',
            field=models.CharField(max_length=254),
        ),
    ]
