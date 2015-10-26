# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-published_date',)},
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='state',
            field=models.CharField(max_length=20, choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Unpublished', 'Unpublished')], default='Draft'),
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=1, to='blog.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='options',
            field=models.ManyToManyField(to='blog.Option'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
    ]
