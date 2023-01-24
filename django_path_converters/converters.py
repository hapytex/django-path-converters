from datetime import date, datetime
import re
from django.apps import apps
from django.contrib.admin.utils import quote
from django.core.exceptions import AppRegistryNotReady
from django.db.models import Model
from django.shortcuts import get_object_or_404
from django.urls import register_converter
from typing import Tuple


class PathConverter(type):
    registered = []
    check_regex = True
    check_examples = True

    @property
    def to_type(cls):
        return cls.accepts[0]

    def __new__(cls, name, bases, attrs):
        if cls.check_regex and 'regex' in attrs:
            # validate regex
            rgx = re.compile(attrs['regex'])
        examples = attrs.get('examples')
        # wrap in a tuple in case of a single example
        if isinstance(examples, str):
            examples = attrs['examples'] = (examples,)
        klass = super().__new__(cls, name, bases, attrs)
        name = attrs.get('name')
        if name:
            register_converter(klass, name)
            cls.registered.append(klass)
        instance = klass()
        if cls.check_examples and examples:
            for example in examples:
                try:
                    result = instance.to_python(example)
                    assert rgx.fullmatch(instance.to_url(result)), f'{result} -> {instance.to_url(result)} ~ {rgx}'
                except (AppRegistryNotReady,):
                    pass
        return klass

    def data_dict(cls):
        return {
            'name': cls.name,
            'type': cls.to_type,
            'examples': '\n'.join(cls.examples),
            'regex': cls.regex,
            'accepts': cls.accepts[1:],
        }


class BaseConverter(metaclass=PathConverter):
    pass_str = True

    def to_python(self, value):
        return value

    def to_url(self, value):
        if not self.pass_str or not isinstance(value, str):
            return self.inner_to_url(value)
        return value

    def inner_to_url(self, value):
        return value


COLON_REGEX = '[:]?'
HOUR_REGEX = r'(?:[0-1]\d|2[0-4])'
MINSEC_REGEX = r'[0-5][0-9]'
TZ_REGEX = rf'(?:Z|[+-]{HOUR_REGEX}{COLON_REGEX}{MINSEC_REGEX})?'
DATE_REGEX = r'[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])'
TIME_REGEX = rf'{HOUR_REGEX}{COLON_REGEX}{MINSEC_REGEX}{COLON_REGEX}{MINSEC_REGEX}{TZ_REGEX}'


class DateTimeConverter(BaseConverter):
    name = 'datetime'
    date_format = '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S', '%Y%m%dT%H%M%S%z', '%Y%m%dT%H%M%S'
    regex = rf'{DATE_REGEX}T{TIME_REGEX}'
    accepts = (datetime, date)
    examples = '2023-01-24T19:21:18Z', '2023-01-24T19:21:18+00:00', '2023-01-24T19:47:58'

    def to_python(self, value, date_format=None):
        date_format = date_format or self.date_format
        if isinstance(date_format, str):
            date_format = (date_format,)
            notLast = False
        else:
            notLast = len(date_format)
        for date_frm in date_format:
            try:
                return datetime.strptime(value, date_frm)
            except ValueError:
                if not notLast:
                    raise
                notLast -= 1

    def inner_to_url(self, value):
        date_format = self.date_format
        if not isinstance(date_format, str):
            date_format = date_format[0]
        return value.strftime(date_format)



class DateConverter(DateTimeConverter):
    name = 'date'
    date_format = '%Y-%m-%d'
    regex = DATE_REGEX
    accepts = (date,)
    examples = '2023-01-21'

    def to_python(self, value, date_format=None):
        return super().to_python(value, date_format=date_format).date()


class MonthConverter(DateConverter):
    name = 'month'
    date_format = '%Y-%m'
    regex = '[0-9]{4}[-](?:0?[1-9]|1[0-2])'
    examples = '2023-01'


class WeekConverter(DateConverter):
    name = 'week'
    date_format = '%G-W%V'
    regex = '[0-9]{4}[-]W(?:0?[1-9]|[1-4][0-9]|5[0-3])'
    examples = '2023-W03'
    week_format = '%u'
    week_day = '1'

    def to_python(self, value):
        return super().to_python(f'{value}{self.week_day}', f'{self.date_format}{self.week_format}')



class DateRangeConverter(DateConverter):
    name = 'date_range'
    regex = f'{DATE_REGEX}/{DATE_REGEX}'
    examples = '2023-01-21/2023-03-25'
    accepts = (tuple[date, date],)

    def to_python(self, value):
        return tuple(map(super().to_python, value.split('/', 1)))

    def inner_to_url(self, value):
        frm, to = value
        return f'{super().inner_to_url(frm)}/{super().inner_to_url(to)}'


class ModelConverter(BaseConverter):
    name = 'model'
    regex = '[^/]+/[^/]+'
    accepts = (Model, type(Model), )
    examples = 'auth/user'

    def to_python(self, value):
        app_label, model_name = value.split('/', 1)
        return apps.get_model(app_label=app_label, model_name=model_name)

    def inner_to_url(self, value):
        if isinstance(value, (Model, type(Model))):
            value = value._meta
        return f'{value.app_label}/{value.model_name}'


class ObjectConverter(ModelConverter):
    name = 'object'
    regex = '[^/]+/[^/]+/[^/]+'
    accepts = (Model,)
    examples = 'auth/user/123', 'auth/user/12'

    def to_python(self, value):
        model, pk = value.rsplit('/', 1)
        model = super().to_python(model)
        return get_object_or_404(model, pk=pk)

    def inner_to_url(self, value):
        return f'{super().inner_to_url(value)}/{quote(value.pk)}'
