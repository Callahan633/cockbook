import re

from bs4 import BeautifulSoup
import requests


class Scraper(object):
    def __init__(self):
        self.target = 'https://eda.ru/recepty?'

    def perform_scraping(self):
        # for counter in range(1, 310):
        content = requests.get(f'{self.target}' + f'page={1}')
        data_for_parsing = BeautifulSoup(content.text, 'lxml')
        meals_for_parsing = data_for_parsing.find_all('h3', class_='horizontal-tile__item-title item-title')
        for header in meals_for_parsing:
            result = header.span.contents
            meal_string, = result
        ingredients_for_parsing = data_for_parsing.find_all('div', class_='ingredients-list__content')
        for div in ingredients_for_parsing:
            result = div.span.contents
            ingredients = result
            print(ingredients)
