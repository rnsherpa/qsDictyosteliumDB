# Generated by Django 3.1.1 on 2021-04-21 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_app', '0008_auto_20210413_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='clone',
            name='mating_type',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Mating Type'),
        ),
    ]