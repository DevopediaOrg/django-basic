# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20151028_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedPost',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('featured', models.BooleanField()),
                ('post', models.ForeignKey(to='blog.Post')),
            ],
        ),
    ]
