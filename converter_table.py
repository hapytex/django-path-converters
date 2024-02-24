# requires Django, pandas, and pytablewriter

from django_path_converters.converters import PathConverter

from pytablewriter import MarkdownTableWriter
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

if __name__ == '__main__':
    df = pd.DataFrame([klass.data_dict() for klass in PathConverter.registered]).sort_values('name')

    df.rename(columns={'accepts': 'also accepts'}, inplace=True)

    # quote_df(df, 'name', '`<', ':…>`')
    # quote_df(df, 'regex')
    # quote_df(df, 'type')
    expl_df(df, 'also accepts')

    # df = df.set_index('name')

    print(df.to_html(formatters={
        'name': partial(codify, lef='<', rig=':…>'),
        'regex': codify,
        'type': codify,
        'also accepts': codify,
        'examples': codify,
    }, index=False, escape=False))
    #MarkdownTableWriter(dataframe=df).write_table()
