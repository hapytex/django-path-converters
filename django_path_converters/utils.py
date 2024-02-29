from re import compile as recompile
from typing import Union, Type

from django.db.models import Model, Manager, QuerySet
from django.db.models.options import Options


REMOVE_CAPTURE_GROUPS = recompile(r'[(][?]P[<][^>]+[>]')

AllItemTypes = Union[Model, Type[Model], Options, Manager, QuerySet]


def get_model(model: AllItemTypes) -> Type[Model]:
    if isinstance(model, Model):  # model *object*
        return type(model)
    elif not issubclass(model, Model):  # not a model class
        return model.model
    return model

def get_queryset(model: AllItemTypes) -> QuerySet:
    if isinstance(model, QuerySet):
        return model
    return get_queryset_or_manager(model).all()

def get_model_or_queryset(model: AllItemTypes) -> Union[Type[Model], QuerySet]:
        if isinstance(model, Model):
            model = type(model)
        elif isinstance(model, Options):
            model = model.model
        return model

def get_queryset_or_manager(model: AllItemTypes, manager_name='_base_manager') -> Union[Manager, QuerySet]:
    if isinstance(model, (QuerySet, Manager)):
        return model
    return getattr(get_model(model), manager_name)

def get_model_options(model: AllItemTypes) -> Options:
    if isinstance(model, Options):
        return model
    return get_model(model)._meta

def strip_capture_groups(pattern: str) -> str:
    return REMOVE_CAPTURE_GROUPS.sub('(?:', pattern)

def wrap_tuple(item) -> tuple:
    if not isinstance(item, (list, tuple)):
        return (item,)
    else:
        return tuple(item)