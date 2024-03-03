from operator import itemgetter

from django.core.management.base import BaseCommand
from django.urls.converters import get_converters
from greenery import parse as gparse


class Command(BaseCommand):
    help = "Look for overlapping URL patterns"

    def handle(self, *args, **options):
        pass
