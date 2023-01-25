from django_path_converters.converters import PathConverter

from pytablewriter import MarkdownTableWriter
import pandas as pd
from django.utils.html import escape
from functools import partial


def quot_type(df, col):
    return df['col']

def quote_df(df, col, lef='`', rig='`'):
    df[col] = lef + df[col].astype(str) + rig

def expl_df(df, col):
    df[col] = df[col].apply(lambda xs: '\n'.join(map(str, xs)))

def codify(text, lef='', rig=''):
    esc = escape(lef+str(text)+rig).replace("\n", "<br>")
    return f'<code>{esc}</code>'

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
