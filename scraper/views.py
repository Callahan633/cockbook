import json

from django.http import JsonResponse, HttpResponse

from scraper.models import Ingredients, Meals, Ingredients_Meals


def ingredients_search(request):
    if request.method == 'GET':
        ingredients = json.loads(request.body)
        ingredients_objects = Ingredients.objects.get(name__in=ingredients['ingredients']).values_list('id', flat=True)
        print(ingredients_objects)
        print(type(ingredients_objects))
        return HttpResponse(ingredients['ingredients'])
