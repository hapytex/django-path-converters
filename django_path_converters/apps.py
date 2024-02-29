from pprint import pprint

from django.apps import AppConfig
from collections import Counter

from django_path_converters.converters import ModelConverter, NullConverterMixin, ModelLoadMixin, BaseConverter


class PathConvertersConfig(AppConfig):
    name = 'django_path_converters'
    verbose_name = 'Django path converters'

    def ready(self):
        import django_path_converters.converters  # noqa
        from django.apps import apps
        from django.urls.converters import StringConverter, UUIDConverter
        from .converters import IntConverter, FullIntConverter, PathConverter, BoolConverter, DateConverter, LazyLoadMixin
        from django.db.models.fields import AutoField, BooleanField, CharField, DateField, FilePathField, IntegerField, UUIDField

        for field, converter in (
                (AutoField, IntConverter),
                (BooleanField, BoolConverter),
                (CharField, StringConverter),
                (DateField, DateConverter),
                (FilePathField, PathConverter),
                (IntegerField, FullIntConverter),
                (UUIDField, UUIDConverter),
        ):
            if not hasattr(field, 'primary_path_converter'):
                setattr(field, 'primary_path_converter', converter)

        counter = Counter(model._meta.model_name for model in apps.get_models())
        for model in apps.get_models():
            for field_rel in model._meta.get_fields():
                field = getattr(field_rel, 'field', field_rel)
                nullable_class = ()
                if field.unique and hasattr(field, 'primary_path_converter'):
                    base_path_converter = field.primary_path_converter
                    if field.null:
                        nullable_class = (NullConverterMixin,)
                    if counter[model._meta.model_name] == 1:
                        names = (f'{model._meta.app_label}_{model._meta.model_name}', f'{model._meta.model_name}')
                    else:
                        names = (f'{model._meta.app_label}_{model._meta.model_name}',)
                    if field.primary_key:
                        suffixes = (f'_{field.name}', '')
                    else:
                        suffixes = (f'_{field.name}',)
                    for _name in names:
                        for suffix in suffixes:
                            class ModelConverter(*nullable_class, ModelLoadMixin, base_path_converter, BaseConverter):  # noqa
                                name = _name
                                model_class = model
                                field_name = field.name
                                name_suffix = suffix
                                from_types = to_types = (model,)

                            class ModelConverter(*nullable_class, LazyLoadMixin, base_path_converter, BaseConverter):  # noqa
                                name = _name
                                model_class = model
                                field_name = field.name
                                name_suffix = suffix
                                from_types = to_types = (model,)