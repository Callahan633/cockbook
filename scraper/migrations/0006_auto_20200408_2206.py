# Generated by Django 3.0.4 on 2020-04-08 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_auto_20200317_1514'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ingredients',
            unique_together={('name', 'measure')},
        ),
    ]