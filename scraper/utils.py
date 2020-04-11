import re
import json
import time

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from bs4 import BeautifulSoup
import requests

from scraper.models import Meals, Ingredients, Ingredients_Meals


class Scraper(object):
    def __init__(self):
        self.target = 'https://eda.ru/recepty?'

    @staticmethod
    def _collect_meals(div):
        result = div.find('h3', class_='horizontal-tile__item-title item-title')
        result = result.span.contents
        meal_string, = result
        meal_string = meal_string.strip()
        return meal_string

    @staticmethod
    def _save_meals(div, meal_string):
        tags_for_parsing = div.find_all('ul', class_='breadcrumbs')
        for tag in tags_for_parsing:
            tags_result = tag.find_all('span')
            categories = re.findall(r'(?<=<span>).*?(?=</span>)', str(tags_result))
            categories_to_str = ''
            for category in categories:
                categories_to_str += f'{category} '
            meal_for_db = Meals(name=meal_string, tags=categories_to_str)
            try:
                meal_for_db.save()
            except IntegrityError:
                pass

    @staticmethod
    def _collect_ingredients(p_tag):
        parsed_dict = json.loads(p_tag['data-ingredient-object'])
        return parsed_dict

    @staticmethod
    def _save_ingredients(parsed_dict):
        ingredients = Ingredients(name=parsed_dict['name'])
        try:
            ingredients.save()
        except IntegrityError:
            pass

    def _get_content(self, counter):
        content = requests.get(f'{self.target}page={counter}')
        data_for_parsing = BeautifulSoup(content.text, 'lxml')
        return data_for_parsing

    def perform_scraping(self):
        global meal, ingredient
        for counter in range(1, 310):
            data_for_parsing = self._get_content(counter)
            meals_for_parsing = data_for_parsing.find_all('div', class_='horizontal-tile__content')
            for div in meals_for_parsing:
                meal_string = self._collect_meals(div)
                self._save_meals(div, meal_string)
                div_content = div.find_all('p', 'ingredients-list__content-item content-item js-cart-ingredients')
                for p_tag in div_content:
                    ingredients = self._collect_ingredients(p_tag)
                    self._save_ingredients(ingredients)
                    measurement_units = ingredients['amount']
                    try:
                        meal = Meals.objects.get(name=meal_string)
                    except ObjectDoesNotExist:
                        pass
                    try:
                        ingredient = Ingredients.objects.get(name=ingredients['name'])
                    except ObjectDoesNotExist:
                        pass
                    if measurement_units is not None:
                        ingredients_meals = Ingredients_Meals(meals_id=meal.id,
                                                              ingredients_id=ingredient.id,
                                                              measure=measurement_units,)
                        try:
                            ingredients_meals.save()
                        except ValidationError:
                            pass
                    else:
                        ingredients_meals = Ingredients_Meals(meals_id=meal.id,
                                                              ingredients_id=ingredient.id,)
                        try:
                            ingredients_meals.save()
                        except ValidationError:
                            pass


def _make_json(item):
    inner_dict = {'name': item.name, 'ingredients': []}
    ingredients_link = Ingredients_Meals.objects.all().filter(meals=item.id)
    for ingredient_link in ingredients_link:
        ingredient_object = Ingredients.objects.get(id=ingredient_link.ingredients.id)
        ingredient_name = ingredient_object.name
        measure = ingredient_link.measure
        inner_dict['ingredients'].append({'name': ingredient_name, 'measure': measure})
    return inner_dict
