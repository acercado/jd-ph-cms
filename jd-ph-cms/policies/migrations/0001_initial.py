# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-04 05:22
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_duration_date_start', models.DateTimeField(blank=True, null=True)),
                ('news_duration_date_end', models.DateTimeField(blank=True, null=True)),
                ('contests_duration_date_start', models.DateTimeField(blank=True, null=True)),
                ('contests_duration_date_end', models.DateTimeField(blank=True, null=True)),
                ('max_answers_per_question', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('map_radius', models.PositiveSmallIntegerField(default=500, validators=[django.core.validators.MinValueValidator(1)])),
                ('admin_email', models.CharField(default='heroku@risingtide.ph', max_length=100)),
                ('messages_new_account', models.TextField(blank=True, null=True)),
                ('messages_new_contest', models.TextField(blank=True, null=True)),
                ('messages_new_loyalty_item', models.TextField(blank=True, null=True)),
                ('messages_winner', models.TextField(blank=True, null=True)),
                ('last_update_datetime', models.DateTimeField(blank=True, null=True)),
                ('claiming_method', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, choices=[('indonesia', 'Indonesia'), ('malaysia', 'Malaysia'), ('philippines', 'Philippines'), ('singapore', 'Singapore')], default='Philippines', max_length=15)),
                ('salesrep_no', models.CharField(blank=True, max_length=200, null=True)),
                ('last_update_by_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cms_policy',
                'verbose_name_plural': 'Policies',
            },
        ),
    ]