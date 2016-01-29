# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-29 10:02
from __future__ import unicode_literals

import cloudinary.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('publish_duration_date_start', models.DateTimeField(blank=True, null=True)),
                ('publish_duration_date_end', models.DateTimeField(blank=True, null=True)),
                ('banner', cloudinary.models.CloudinaryField(max_length=255, verbose_name='banner')),
                ('points', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_type', models.CharField(default='Contest', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=False)),
                ('category', models.CharField(blank=True, default='contests', max_length=50, null=True)),
                ('question_title', models.TextField(max_length=300, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myuser.MyUser')),
            ],
            options={
                'db_table': 'cms_contest',
                'verbose_name_plural': 'Contests',
            },
        ),
    ]