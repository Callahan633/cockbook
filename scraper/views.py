import json
import operator
from functools import reduce

from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q

from scraper.models import Ingredients, Meals, Ingredients_Meals
from scraper.utils import _make_json


def ingredients_search(request):
    if request.method == 'POST':
        ingredients_for_search = json.loads(request.body)
        if "" or " " in ingredients_for_search['ingredients']:
            return HttpResponseBadRequest()
        else:
            ingredients_objects_ids = Ingredients.objects.filter(reduce(operator.or_, (Q(name__icontains=x) for x in ingredients_for_search['ingredients']))).values_list('id', flat=True)
            meals_link = Ingredients_Meals.objects.all().filter(ingredients__in=list(ingredients_objects_ids)).values_list('meals', flat=True)
            meals = Meals.objects.all().filter(id__in=list(meals_link)).values_list('id', flat=True)[:100]
            meals_for_json = {'recipes': []}
            for item in Meals.objects.all().filter(id__in=meals):
                inner_dict = _make_json(item)
                meals_for_json['recipes'].append(inner_dict)
        return JsonResponse(meals_for_json)


def meals_search(request):
    if request.method == 'POST':
        meals_for_search = json.loads(request.body)
        if "" or " " in meals_for_search['meals']:
            return HttpResponseBadRequest()
        else:
            meals_objects_ids = Meals.objects.filter(reduce(operator.or_, (Q(name__icontains=x) for x in meals_for_search['meals']))).values_list('id', flat=True)
            meals_for_json = {'recipes': []}
            for item in Meals.objects.all().filter(id__in=list(meals_objects_ids)):
                inner_dict = _make_json(item)
                meals_for_json['recipes'].append(inner_dict)
        return JsonResponse(meals_for_json)
