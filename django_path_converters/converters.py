from datetime import date, datetime
import re
from enum import Enum
from functools import partial
from collections import namedtuple

from django.contrib.admin.utils import quote
from django.core.exceptions import AppRegistryNotReady
from django.core.validators import EmailValidator
from django.db.models import Model, Q
from django.db.models.enums import ChoicesMeta
from django.db.models.query import QuerySet
from django.db.models.manager import Manager
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import register_converter
from django.urls.converters import DEFAULT_CONVERTERS, SlugConverter, IntConverter, StringConverter, UUIDConverter
from django.utils.text import slugify
from django.db.models.options import Options

from django_path_converters.lazymodelobject import ModelLazyObject

import json

from django_path_converters.utils import strip_capture_groups


class PathConverter(type):
    registered = []
    check_regex = True
    check_examples = True

    @property
    def to_type(cls):
        if cls.accepts:
            return cls.accepts[0]

    def __new__(cls, name, bases, attrs):
        if cls.check_regex and 'regex' in attrs:
            # validate regex
            rgx = re.compile(attrs['regex'])
            attrs['regex'] = rgx.pattern  # might be simplified (in future)
        if 'accepts' in attrs and not isinstance(attrs['accepts'], (list, tuple)):
            attrs['accepts'] = (attrs['accepts'],)
        examples = attrs.get('examples')
        # wrap in a tuple in case of a single example
        if isinstance(examples, str):
            examples = attrs['examples'] = (examples,)
        klass = super().__new__(cls, name, bases, attrs)
        name = attrs.get('name')
        if name:
            klass.name = name = f'{getattr(klass, "name_prefix", "")}{name}{getattr(klass, "name_suffix", "")}'
            register_converter(klass, name)
            cls.registered.append(klass)
        instance = klass()
        # if cls.check_examples and examples:
        #     for example in examples:
        #         try:
        #             assert rgx.fullmatch(example), f'{example} ~ {rgx.pattern}'
        #             result = instance.to_python(example)
        #             assert rgx.fullmatch(instance.to_url(result)), f'{result} -> {instance.to_url(result)} ~ {rgx}'
        #         except (AppRegistryNotReady,):
        #             pass
        return klass

    def data_dict(cls):
        return {
            'name': cls.name,
            'type': cls.to_type,
            'examples': '\n'.join(cls.examples),
            'regex': cls.regex,
            'accepts': cls.accepts[1:],
        }


    def __repr__(cls):
        if hasattr(cls, 'name'):
            return f'<{cls.name}:…>'
        else:
            return super().__repr__()


class BaseConverter(metaclass=PathConverter):
    name_prefix = ''
    name_suffix = ''
    pass_str = True

    def to_python(self, value):
        return value

    def to_url(self, value):
        if not self.pass_str or not isinstance(value, str):
            return self.inner_to_url(value)
        return value

    def inner_to_url(self, value):
        return value

    def __repr__(self):
        return f'<{self.name}:…>'


class NullConverterMixin:
    use_explicit_null = True
    nulls = {'null', 'none'}
    explicit_null_regex = '[Nn][Uu][Ll]{2}|[Nn][Oo][Nn][Ee]'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.use_explicit_null:
            cls.regex = f'(?:{cls.regex})||{cls.explicit_null_regex}'
            cls.examples = *cls.examples, '', 'null', 'NULL', 'NONE', 'None', 'none'
        else:
            cls.regex = f'(?:{cls.regex})|'
            cls.examples = *cls.examples, ''

    def to_python(self, value):
        if value and (not self.use_explicit_null or value.casefold() not in self.nulls):
            return super().to_python(value)

    def to_url(self,value):
        if value is not None:
            return super().to_url(value)
        elif self.use_explicit_null:
            return 'null'
        else:
            return ''


class BoolConverter(BaseConverter):
    yeas = {'yes', 'true', 't', 'y', '1', 'on'}
    regex = '[Yy]([Ee][Ss])?|[Tt]([Rr][Uu][Ee])?|[Oo][Nn]|1|[Ff]([Aa][Ll][Ss][Ee])?|[Nn][Oo]?|[Oo][Ff][Ff]|0'
    name = 'bool'
    accepts = object
    examples = 'True', 'False', '1', '0', 'T', 'F', 'on', 'oFF', 'yes', 'NO'

    def to_python(self, value):
        return value.casefold() in self.yeas

    def to_url(self, value):
        return json.dumps(bool(value))


class NullBoolConverter(NullConverterMixin, BoolConverter):
    name = 'nullbool'


class MetaCombinedConverter(type(BaseConverter)):
    path_separator = '/'
    path_separator_regex = '/'
    tuple_constructor = namedtuple

    def __new__(cls, name, bases, attrs):
        if 'name' in attrs:
            subs = {k: v() for k,v in attrs.items() if isinstance(v, type) and issubclass(v, (BaseConverter, *map(type, DEFAULT_CONVERTERS.values())))}
            attrs['_subconverters'] = subs
            constructor = attrs['constructor'] = cls.tuple_constructor(attrs['name'], list(subs))
            attrs['accepts'] = (constructor,)
            attrs['regex'] = cls.path_separator_regex.join([f'(?P<{k}>{strip_capture_groups(v.regex)})' for k, v in subs.items()])
            return super().__new__(cls, name, bases, attrs)
        return super().__new__(cls, name, bases, attrs)

class CombinedBaseConverter(BaseConverter, metaclass=MetaCombinedConverter):
    def to_python(self, value):
        _match = re.match(self.regex, value)
        return self.constructor(**{k: v.to_python(_match.group(k)) for k, v in self._subconverters.items()})

    def to_url(self, value):
        return type(self).path_separator.join([v.to_url(getattr(value, k)) for k, v in self._subconverters.items()])


COLON_REGEX = '[:]?'
HOUR_REGEX = r'(?:[0-1]\d|2[0-4])'
MINSEC_REGEX = r'[0-5][0-9]'
TZ_REGEX = rf'(?:Z|[+-]{HOUR_REGEX}{COLON_REGEX}{MINSEC_REGEX})?'
DATE_REGEX = r'[0-9]{4}[-](?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])'
TIME_REGEX = rf'{HOUR_REGEX}{COLON_REGEX}{MINSEC_REGEX}{COLON_REGEX}{MINSEC_REGEX}{TZ_REGEX}'


class AutoSlugConverter(BaseConverter, SlugConverter):
    pass_str = False
    name = 'autoslug'
    accepts = (str, Model)
    allow_unicode = False
    slug_field = 'slug'
    regex = SlugConverter.regex
    examples = 'this-is-a-slug', 'slugifying-this-str'

    def to_url(self, value):
        value = str(getattr(value, self.slug_field, value))
        return slugify(value, allow_unicode=self.allow_unicode)

class UnicodeAutoSlugConverter(AutoSlugConverter):
    name = 'autoslugunicode'
    allow_unicode = True

class FullIntConverter(IntConverter, BaseConverter):
    name = 'fullint'
    regex = f'[+-]?{IntConverter.regex}'
    examples = '-12', '14', '25'
    accepts = (int,)

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
            notLast = len(date_format) - 1
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

    def to_python(self, value, date_format=None):
        return super().to_python(f'{value}{self.week_day}', date_format or f'{self.date_format}{self.week_format}')


class DateRangeConverter(CombinedBaseConverter):
    name = 'daterange'
    from_date = DateConverter
    to_date = DateConverter
    examples = '1958-3-25/2019-11-25'
    accepts = (namedtuple, )


class ModelConverter(BaseConverter):
    name = 'model'
    regex = '[^/]+/[^/]+'
    accepts = (type(Model), Model, Options, QuerySet, Manager)
    examples = 'auth/user'

    def to_python(self, value):
        from django.apps import apps
        app_label, model_name = value.split('/', 1)
        try:
            return apps.get_model(app_label=app_label, model_name=model_name)
        except LookupError as e:
            # use a ValueError such that Django can continue looking for a match
            raise ValueError(*e.args)

    def inner_to_url(self, value):
        if isinstance(value, (Manager, QuerySet)):
            value = value.model
        if isinstance(value, (Model, type(Model))):
            value = value._meta
        return f'{value.app_label}/{value.model_name}'


class ObjectConverter(ModelConverter):
    name = 'eagerobject'
    regex = '[^/]+/[^/]+/[^/]+'
    accepts = (Model,)
    examples = 'auth/group/123', 'auth/user/12'
    manager = None

    def create_object(self, model, pk):
        return get_object_or_404(model, pk=pk)

    def to_python(self, value):
        model, pk = value.rsplit('/', 1)
        model = super().to_python(model)
        if self.manager is not None:
            model = getattr(model, self.manager)
        try:
            return get_object_or_404(model, pk=pk)
        except Http404 as e:
            raise ValueError(*e.args)

    def inner_to_url(self, value):
        return f'{super().inner_to_url(value)}/{quote(value.pk)}'


class LazyObjectConverter(ObjectConverter):
    name = 'object'
    pk_field = 'pk'
    check_field = True

    def create_object(self, model, pk):
        return ModelLazyObject(model, pk, pk_field=self.pk_field, check_field=self.check_field)

class ChoicesConverter(BaseConverter):
    name_prefix = 'choices_'

    def __init_subclass__(cls, choices, **kwargs):
        if isinstance(choices, ChoicesMeta):
            pass  # TODO
        super().__init_subclass__(cls, **kwargs)


class EmailConverter(BaseConverter):
    name = 'email'
    regex = f'.*' # f'(?:{EmailValidator.user_regex.pattern})@(?:{EmailValidator.domain_regex.pattern})'
    accepts = str
    examples = ('info@djangoproject.com', 'test@foo.org')

class EnumConverter(BaseConverter):
    name_prefix = 'enum_'
    enum_class = None

    def __init_subclass__(cls, enum_class=None, name=None, **kwargs):
        cls.enum_class = enum_class or cls.enum_class
        if not issubclass(enum_class, Enum):
            raise ValueError('The enum_class must be a subclass of Enum')
        setattr(cls, 'regex', '|'.join(re.escape(v) for v in enum_class.values))
        super().__init_subclass__(**kwargs)

    def to_python(self, value):
        if isinstance(value, str):
            return self.enum_class(value)
        return super().to_python(value)

    def inner_to_url(self, value):
        if isinstance(value, self.enum_class):
            return value.value
        return value


class ModelLoadMixin:
    name_prefix = 'eager_'
    model_class = None
    field_name = None
    
    @property
    def accepts(self):
        return (self.model_class,)

    def to_python(self, value):
        try:
            return get_object_or_404(self.model_class, Q((self.field_name, super().to_python(value))))
        except self.model_class.DoesNotExist as e:
            raise ValueError(*e.args)

    def to_url(self, value):
        return super().to_url(getattr(value, self.field_name, value))



class LazyLoadMixin:
    model_class = None
    field_name = None
    check_field = True

    @property
    def accepts(self):
        return (self.model_class,)

    def to_python(self, value):
        return ModelLazyObject(self.model_class, super().to_python(value), pk_field=self.field_name, check_field=self.check_field)

    def to_url(self, value):
        return super().to_url(getattr(value, self.field_name, value))