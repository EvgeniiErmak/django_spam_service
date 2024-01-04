# Generated by Django 4.2.9 on 2024-01-04 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_service', '0002_mailinglist_body_mailinglist_subject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ['-attempt_time'], 'verbose_name': 'Лог', 'verbose_name_plural': 'Логи'},
        ),
        migrations.RemoveField(
            model_name='log',
            name='message',
        ),
        migrations.AddField(
            model_name='log',
            name='mailing_list',
            field=models.ForeignKey(default=12345, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='mailing_service.mailinglist', verbose_name='Рассылка'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='attempt_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки'),
        ),
        migrations.AlterField(
            model_name='log',
            name='response',
            field=models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера'),
        ),
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.CharField(max_length=255, verbose_name='Статус попытки'),
        ),
    ]
