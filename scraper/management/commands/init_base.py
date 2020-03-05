from django.core.management.base import BaseCommand

from scraper.views import Scraper


class Command(BaseCommand):
    def handle(self, *args, **options):
        s = Scraper()
        s.perform_scraping()
