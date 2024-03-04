from operator import itemgetter

from django.core.management.base import BaseCommand
from django.urls.converters import get_converters


class Command(BaseCommand):
    help = "Search and list path converters"

    def handle(self, *args, **options):
        items = sorted(get_converters().items(), key=itemgetter(0))
        lenk = max(map(len, map(itemgetter(0), items))) + 5
        for key, val in items:
            print(f'\x1b[1m<{key}:…>\x1b[0m{" "*(lenk - len(key))}{getattr(val, "help", "")}')