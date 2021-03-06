# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_tag_app', '0002_auto_20170625_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='headtag',
            name='detail_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='headtag',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True, protocol='IPv4'),
        ),
        migrations.AlterField(
            model_name='headtag',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
