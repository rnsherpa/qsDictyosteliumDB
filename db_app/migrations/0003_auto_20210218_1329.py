# Generated by Django 3.1.1 on 2021-02-18 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_app', '0002_auto_20201204_0109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clone',
            name='isFarmer',
        ),
        migrations.AddField(
            model_name='clone',
            name='burkSpecies',
            field=models.CharField(blank=True, max_length=50, verbose_name='Burkholderia Species'),
        ),
        migrations.AddField(
            model_name='clone',
            name='chlamHap',
            field=models.CharField(blank=True, max_length=10, verbose_name='Neochlamydia Haplotype'),
        ),
        migrations.AddField(
            model_name='clone',
            name='endoHapID',
            field=models.CharField(blank=True, max_length=50, verbose_name='Endosymbiont Haplotype ID'),
        ),
        migrations.AddField(
            model_name='clone',
            name='endoSeqHit',
            field=models.CharField(blank=True, max_length=100, verbose_name='Endosymbiont 16S Sequence Hit'),
        ),
        migrations.AddField(
            model_name='clone',
            name='isAmo',
            field=models.BooleanField(blank=True, null=True, verbose_name='Amoebophilis Endosymbiont'),
        ),
        migrations.AddField(
            model_name='clone',
            name='isChlam',
            field=models.BooleanField(blank=True, null=True, verbose_name='Neochlamydia Endosymbiont'),
        ),
        migrations.AddField(
            model_name='clone',
            name='sequenced',
            field=models.CharField(blank=True, max_length=20, verbose_name='Sequenced'),
        ),
        migrations.AddField(
            model_name='clone',
            name='violHapGrp',
            field=models.CharField(blank=True, max_length=10, verbose_name='vio.hap.grp'),
        ),
        migrations.AlterField(
            model_name='clone',
            name='species',
            field=models.CharField(max_length=50, verbose_name='Species'),
        ),
    ]
