import re
import json
import time

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
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
            meal = Meals(name=meal_string, tags=categories_to_str)
            try:
                meal.save()
            except IntegrityError:
                pass

    @staticmethod
    def _collect_ingredients(p_tag):
        parsed_dict = json.loads(p_tag['data-ingredient-object'])
        return parsed_dict

    @staticmethod
    def _save_ingredients(parsed_dict):
        regexp = re.compile(r"(?<=\s)\D+")
        measurement_units = re.search(regexp, parsed_dict['amount'])
        if measurement_units is not None:
            ingredients = Ingredients(name=parsed_dict['name'],
                                      measure=measurement_units.group(0))
            try:
                ingredients.save()
            except IntegrityError:
                pass
        else:
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
        for counter in range(1, 310):
            time.sleep(0.5)
            data_for_parsing = self._get_content(counter)
            meals_for_parsing = data_for_parsing.find_all('div', class_='horizontal-tile__content')
            for div in meals_for_parsing:
                meal_string = self._collect_meals(div)
                self._save_meals(div, meal_string)
                div_content = div.find_all('p', 'ingredients-list__content-item content-item js-cart-ingredients')
                for p_tag in div_content:
                    ingredients = self._collect_ingredients(p_tag)
                    self._save_ingredients(ingredients)

    def make_links(self):
        for counter in range(1, 310):
            time.sleep(0.5)
            data_for_parsing = self._get_content(counter)
            meals_for_parsing = data_for_parsing.find_all('div', class_='horizontal-tile__content')
            for div in meals_for_parsing:
                meal_string = self._collect_meals(div)
                div_content = div.find_all('p', 'ingredients-list__content-item content-item js-cart-ingredients')
                for p_tag in div_content:
                    ingredients = self._collect_ingredients(p_tag)
                    amount = re.search(r'(\d+(,\d+)?)', ingredients['amount'])
                    if amount is not None:
                        try:
                            meal = Meals.objects.get(name=meal_string)
                        except ObjectDoesNotExist:
                            pass
                        try:
                            ingredient = Ingredients.objects.get(name=ingredients['name'])
                        except ObjectDoesNotExist:
                            pass
                            converted_to_decimal = re.sub(r',', '.', amount.group(0))
                            ingredients_meals = Ingredients_Meals(meals_id=meal.id,
                                                                  ingredients_id=ingredient.id,
                                                                  amount=converted_to_decimal)
                            try:
                                ingredients_meals.save()
                            except IntegrityError:
                                pass
