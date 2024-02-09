from re import compile as recompile
from typing import Union

from django.db.models import Model, Manager, QuerySet
from django.db.models.options import Options


REMOVE_CAPTURE_GROUPS = recompile(r'[(][?]P[<][^>]+[>]')


def get_model(model: Union[Model, type(Model), Manager, QuerySet]) -> Model:
    if not issubclass(model, Model):
        return model.model
    return model

def get_queryset(model: Union[Model, type(Model), Manager, QuerySet]) -> QuerySet:
    if isinstance(model, QuerySet):
        return model
    return get_queryset_or_manager(model).all()

def get_queryset_or_manager(model: Union[Model, type(Model), Manager, QuerySet]) -> QuerySet:
    if isinstance(model, (QuerySet, Manager)):
        return model
    if isinstance(model, Model):  # not a model class
        model = type(model)
    return model._base_manager

def get_model_options(model: Union[Model, Options, type(Model), Manager, QuerySet]) -> Options:
    if isinstance(model, Options):
        return model
    return get_model(model)._meta

def strip_capture_groups(pattern: str):
    return REMOVE_CAPTURE_GROUPS.sub('(?:', pattern)