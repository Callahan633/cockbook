# Generated by Django 3.0.4 on 2020-03-05 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20200305_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meals',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
