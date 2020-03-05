# Generated by Django 3.0.4 on 2020-03-05 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('measure', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Meals',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(blank=True, max_length=255)),
                ('ingredients', models.ManyToManyField(to='scraper.Ingredients')),
            ],
        ),
    ]
