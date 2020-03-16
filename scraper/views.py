import re
import json
import time

from django.db.utils import IntegrityError

from bs4 import BeautifulSoup
import requests

from scraper.models import Meals, Ingredients, Ingredients_Meals


class Scraper(object):
    def __init__(self):
        self.target = 'https://eda.ru/recepty?'

    def perform_scraping(self):
        for counter in range(1, 310):
            time.sleep(1)
            content = requests.get(f'{self.target}' + f'page={counter}')
            data_for_parsing = BeautifulSoup(content.text, 'lxml')
            meals_for_parsing = data_for_parsing.find_all('div', class_='horizontal-tile__content')
            for div in meals_for_parsing:
                result = div.find('h3', class_='horizontal-tile__item-title item-title')
                result = result.span.contents
                meal_string, = result
                meal_string = meal_string.strip()
                tags_for_parsing = div.find_all('ul', class_='breadcrumbs')
                for tag in tags_for_parsing:
                    tags_result = tag.find_all('span')
                    categories = re.findall(r'(?<=<span>).*?(?=</span>)', str(tags_result))
                    categories_to_str = ''
                    for category in categories:
                        categories_to_str += category + ', '
                    meal = Meals(name=meal_string, tags=categories_to_str)
                    try:
                        meal.save()
                    except IntegrityError:
                        pass
                div_content = div.find_all('p', 'ingredients-list__content-item content-item js-cart-ingredients')
                for p_tag in div_content:
                    parsed_dict = json.loads(p_tag['data-ingredient-object'])
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
                    amount = re.search(r'(\d+(,\d+)?)', parsed_dict['amount'])
                    ingredients_meals = Ingredients_Meals(meals_id=meal.id,
                                                          ingredients_id=ingredients.id,
                                                          amount=amount.group(0))
                    try:
                        ingredients_meals.save()
                    except IntegrityError:
                        pass
