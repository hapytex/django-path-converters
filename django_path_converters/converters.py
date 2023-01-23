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
            re.compile(attrs['regex'])
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
                except (AppRegistryNotReady,):
                    pass
        return klass

    def data_dict(cls):
        return {
            'name': cls.name,
            'regex': cls.regex,
            'examples': '\n'.join(cls.examples),
            'type': cls.to_type,
            'accepts': cls.accepts,
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


class DateConverter(BaseConverter):
    name = 'date'
    date_format = '%Y-%m-%d'
    regex = '[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])'
    accepts = (date,)
    examples = '2023-01-21'

    def to_python(self, value, date_format=None):
        return datetime.strptime(value, date_format or self.date_format).date()

    def inner_to_url(self, value):
        return value.strftime(self.date_format)


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
    regex = '/'.join((DateConverter.regex,)*2)
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
