# Generated by Django 3.1.1 on 2021-02-25 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_app', '0004_auto_20210224_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clone',
            name='altID',
            field=models.CharField(max_length=20, verbose_name='Alternate ID'),
        ),
    ]