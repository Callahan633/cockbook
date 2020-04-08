from django.core.management.base import BaseCommand

from scraper.utils import Scraper


class Command(BaseCommand):
    def handle(self, *args, **options):
        s = Scraper()
        s.make_links()
