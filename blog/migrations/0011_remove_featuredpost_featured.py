# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_featuredpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featuredpost',
            name='featured',
        ),
    ]
