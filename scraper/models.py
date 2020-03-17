from django.db import models


class Ingredients(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, unique=True)
    measure = models.CharField(max_length=100, blank=True)


class Meals(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, unique=True)
    tags = models.CharField(max_length=255, blank=True)


class Ingredients_Meals(models.Model):
    id = models.BigAutoField(primary_key=True)
    meals = models.ForeignKey(to=Meals, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(to=Ingredients, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=1, max_digits=5, blank=True)
    additional_info = models.CharField(max_length=255, blank=True)
