# Generated by Django 4.1.3 on 2023-04-17 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_free_inplay_odds_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vip_odds',
            name='games',
            field=models.ManyToManyField(blank=True, to='backend.vip_games'),
        ),
    ]
