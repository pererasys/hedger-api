# Generated by Django 3.1.1 on 2020-09-23 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_remove_report_macd'),
        ('users', '0002_auto_20200922_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='watch_list',
            field=models.ManyToManyField(blank=True, related_name='watched_by', through='users.WatchedAsset', to='assets.Asset'),
        ),
    ]
