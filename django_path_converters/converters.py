from datetime import date
import re
from django.apps import apps
from django.db.models import Model
from django.shortcuts import get_object_or_404
from django.urls import register_converter


class PathConverter(type):
    def __new__(cls, name, bases, attrs):
        if 'regex' in attrs:
            # validate regex
            re.compile(attrs['regex'])
        klass = super().__new__(name, bases, attrs)
        if 'name' in attrs:
            register_converter(klass, attrs[name])
        return klass


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

    def to_python(self, value):
        return datetime.strptime(value, self.date_format).date()

    def inner_to_url(self, value):
        return value.strftime(self.date_format)


class MonthConverter(DateConverter):
    name = 'month'
    date_format = '%Y-%m'
    regex = '[0-9]{4}[-](?:0?[1-9]|1[0-2])'


class WeekConverter(DateConverter):
    name = 'week'
    date_format = '%Y-W%V'
    regex = '[0-9]{4}[-]W(?:0?[1-9]|[1-4][0-9]|5[0-3])'


class DateRangeConverter(BaseConverter):
    name = 'date_range'
    regex = '/'.join((DateConverter.regex,)*2)

    def to_python(self, value):
        return tuple(map(super().to_python, value.split('/', 1)))

    def inner_to_url(self, value):
        frm, to = value
        return f'{super().inner_to_url(frm)}/{super().inner_to_url(to)}'


class ModelConverter(BaseConverter):
    name = 'model'
    regex = '[^/]+/[^/]+'
    accepts = (Model, type(Model), )

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

    def to_python(self, value):
        model, pk = value.rsplit('/', 1)
        model = super().to_python(model)
        return get_object_or_404(model, pk=pk)

    def inner_to_url(self, value):
        return f'{super().inner_to_url(value)}/{value.pk}'
