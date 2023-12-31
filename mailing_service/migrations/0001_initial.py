# Generated by Django 5.0 on 2023-12-29 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('full_name', models.CharField(max_length=255)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_time', models.DateTimeField()),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=20)),
                ('status', models.CharField(choices=[('created', 'Created'), ('started', 'Started'), ('completed', 'Completed')], max_length=20)),
                ('clients', models.ManyToManyField(to='mailing_service.client')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('mailing_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing_service.mailinglist')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
                ('response', models.TextField()),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing_service.message')),
            ],
        ),
    ]
