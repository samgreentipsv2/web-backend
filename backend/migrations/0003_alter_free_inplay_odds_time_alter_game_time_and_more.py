# Generated by Django 4.1.3 on 2023-04-17 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_free_inplay_odds_time_alter_game_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='free_inplay_odds',
            name='time',
            field=models.DateTimeField(blank=True, default='Mon Apr 17 02:11:21 2023'),
        ),
        migrations.AlterField(
            model_name='game',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vip_games',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
