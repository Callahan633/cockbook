# Generated by Django 3.0.4 on 2020-04-09 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0007_auto_20200408_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredients_meals',
            name='amount',
        ),
    ]