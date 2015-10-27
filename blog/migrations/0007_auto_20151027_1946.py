# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20151026_0949'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Topic',
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ('name',)},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='category',
            new_name='topic',
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='.', null=True),
        ),
    ]
