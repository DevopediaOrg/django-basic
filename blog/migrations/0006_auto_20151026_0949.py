# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20151026_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='options',
            field=models.ManyToManyField(blank=True, to='blog.Option'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag'),
        ),
    ]
