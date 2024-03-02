from django.core.management.base import BaseCommand
from django.urls import get_resolver
from greenery import parse as gparse


class Command(BaseCommand):
    help = "Search if two or more URLs overlap"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("--regex", type=gparse)

    def produce_regexes(self, resolver, prefix):
        regex = f'{prefix}{resolver.pattern.regex}'
        if resolver.callback is not None:
            yield regex
        for subresolver in resolver.url_patterns:
            yield from self.produce_regexes(subresolver, regex)

    def handle(self, *args, **options):
        resolver = get_resolver()
        for regex in self.produce_regexes(resolver, ''):
            print(regex)