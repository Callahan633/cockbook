import json
import operator
from functools import reduce

from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from scraper.models import Ingredients, Meals, Ingredients_Meals


def ingredients_search(request):
    if request.method == 'POST':
        ingredients_for_search = json.loads(request.body)
        ingredients_objects_ids = Ingredients.objects.filter(reduce(operator.and_, (Q(name__icontains=x) for x in ingredients_for_search['ingredients']))).values_list('id', flat=True)
        meals_link = Ingredients_Meals.objects.all().filter(ingredients__in=list(ingredients_objects_ids)).values_list('meals', flat=True)
        meals = Meals.objects.all().filter(id__in=list(meals_link)).values_list('id', flat=True)[:100]
        meals_for_json = {'recipes': []}
        for item in Meals.objects.all().filter(id__in=meals):
            inner_dict = {'name': item.name, 'ingredients': []}
            ingredients_link = Ingredients_Meals.objects.all().filter(meals=item.id)
            for ingredient_link in ingredients_link:
                ingredient_object = Ingredients.objects.get(id=ingredient_link.ingredients.id)
                ingredient_name = ingredient_object.name
                measure = ingredient_link.measure
                inner_dict['ingredients'].append({'name': ingredient_name, 'measure': measure})
            meals_for_json['recipes'].append(inner_dict)
        return JsonResponse(meals_for_json)


def meals_search(request):
    if request.method == 'POST':
        meals_for_search = json.loads(request.body)
        meals_objects_ids = Meals.objects.filter(name__icontains=meals_for_search['meals']).values_list('id', flat=True)
        ingredients_link = Ingredients_Meals.objects.all().filter(meals__in=list(meals_objects_ids)).values_list('meals', flat=True)
        ingredients = Ingredients_Meals.objects.all().filter(id__in=list(ingredients_link)).values_list('')