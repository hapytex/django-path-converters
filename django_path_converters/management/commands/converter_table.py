from django.core.management.base import BaseCommand
from django.db.models import Count
from django_path_converters.converters import PathConverter

import pandas as pd
from django.utils.html import escape
from functools import partial
from types import GenericAlias


def str_type(typ):
    if isinstance(typ, GenericAlias):
        return str(typ)
    if typ.__module__ and typ.__module__ != 'builtins':
        return f'{typ.__module__}.{typ.__qualname__}'
    return typ.__qualname__


def to_str(text):
    if isinstance(text, type):
        return str_type(text)
    if isinstance(text, (tuple, list)):
        maps = tuple(map(to_str, text))
        if len(maps) == 1:
            return f'({maps[0]}, )'
        return f"({', '.join(maps)})"
    return str(text)


def quot_type(df, col):
    return df['col']

def quote_df(df, col, lef='`', rig='`'):
    df[col] = lef + df[col].astype(str) + rig

def expl_df(df, col):
    df[col] = df[col].apply(lambda xs: '\n'.join(map(str, xs)))

def codify(text, lef='', rig=''):
    text = to_str(text)
    if text:
        return '<br/>'.join(f'<code>{escape(lef+lin+rig)}</code>' for lin in text.split('\n'))
    return ''


class Command(BaseCommand):
    help = "Create a table of the registered path converters"

    def handle(self, *args, **options):
        df = pd.DataFrame([klass.data_dict() for klass in PathConverter.registered]).sort_values('name')

        # df.rename(inplace=True)

        # quote_df(df, 'name', '`<', ':…>`')
        # quote_df(df, 'regex')
        # quote_df(df, 'type')
        expl_df(df, 'to_types')
        expl_df(df, 'from_types')

        # df = df.set_index('name')

        print(df.to_html(formatters={
            'name': partial(codify, lef='<', rig=':…>'),
            'regex': codify,
            'to_types': codify,
            'from_types': codify,
            'examples': codify,
        }, index=False, escape=False))