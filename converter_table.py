from django_path_converters.converters import PathConverter

from pytablewriter import MarkdownTableWriter
import pandas as pd

df = pd.DataFrame([klass.data_dict() for klass in PathConverter.registered])

MarkdownTableWriter(dataframe=df).write_table()
