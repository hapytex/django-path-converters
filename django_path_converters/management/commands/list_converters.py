from django.core.management.base import BaseCommand
from tabulate import tabulate

from django_path_converters.converters import PathConverter


def summarize_converters(*path_converters):
    data = [converter.data_dict() for converter in PathConverter.registered]
    idx = {k: None for converter in data for k in converter}
    table = [[converter.get(k) for k in idx] for converter in data]
    return tabulate(table, headers=idx, tablefmt='pretty', maxcolwidths=128)

class Command(BaseCommand):
    help = "List all path converters"

    def handle(self, *args, **options):
        converters = [klass.data_dict() for klass in PathConverter.registered]
        return print(summarize_converters(*converters))