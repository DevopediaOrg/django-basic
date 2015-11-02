# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_remove_featuredpost_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featuredpost',
            name='post',
        ),
        migrations.DeleteModel(
            name='FeaturedPost',
        ),
    ]
