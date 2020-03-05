from django.db import models


class Ingredients(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    measure = models.CharField(max_length=100, blank=True)


class Meals(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField(Ingredients)
