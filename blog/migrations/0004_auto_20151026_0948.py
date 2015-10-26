# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20151026_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='options',
            field=models.ManyToManyField(to='blog.Option', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
