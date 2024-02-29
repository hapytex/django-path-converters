from django.core.management.base import BaseCommand
from django.db.models import Count
from catalog.models import SubGroup, Regime
from catalog.cache import get_cached_frames


class Command(BaseCommand):
    help = "Fill caches"