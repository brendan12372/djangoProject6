# Generated by Django 4.0.2 on 2022-03-03 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topTen', '0007_sectoroptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectoroptions',
            name='dir',
            field=models.CharField(blank=True, default='up', max_length=200),
        ),
        migrations.AlterField(
            model_name='sectoroptions',
            name='sortBy',
            field=models.CharField(blank=True, default='yearReturn', max_length=200),
        ),
    ]