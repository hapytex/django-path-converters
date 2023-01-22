from django_path_converters.converters import PathConverter

from pytablewriter import MarkdownTableWriter
import pandas as pd

def quote_df(df, col):
    df[col] = '`' + df[col].astype(str) + '`'

def expl_df(df, col):
    df[col] = df[col].join('\n')

df = pd.DataFrame([klass.data_dict() for klass in PathConverter.registered]).sort_values('name')

quote_df(df, 'name')
quote_df(df, 'regex')
quote_df(df, 'type')

MarkdownTableWriter(dataframe=df).write_table()
