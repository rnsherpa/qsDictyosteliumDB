# Generated by Django 3.1.1 on 2021-05-20 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_app', '0002_auto_20210520_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='doi',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='DOI'),
        ),
    ]