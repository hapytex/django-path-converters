from django.db.models import Model, QuerySet, Manager, Q
from django.db.models.options import Options
from django.shortcuts import get_object_or_404
from django.utils.functional import LazyObject

from django_path_converters.utils import get_model_options, get_model, get_queryset, get_model_or_queryset


class ModelLazyObject(LazyObject):
    # TODO: setters for the fields that are known
    # set class fields, to avoid infinite loops when setting attributes
    _pk_field = 'pk'
    _pk = None
    _model_or_queryset = None
    _model = None
    _is_pk = True

    @property
    def __class__(self):
        # used for the isinstance check, this prevents us from querying
        # when performing isinstance functions
        return self._model

    def __init__(self, model_or_queryset, pk, pk_field='pk', check_field=True):
        assert isinstance(model_or_queryset, (type(Model), Model, Options, Manager, QuerySet))
        model_or_queryset = get_model_or_queryset(model_or_queryset)
        # prevent loading the object by using a setter
        dic = self.__dict__
        model = get_model(model_or_queryset)
        dic.update(_model_or_queryset=model_or_queryset, _pk=pk, _model=model)
        # prevent adding attributes to instances
        if pk_field != 'pk':
            dic.update(_pk_field=pk_field)
        if check_field:
            # check if the model indeed can resolve the field, will *NOT* make a query
            get_queryset(model_or_queryset).filter(Q((pk_field, pk)))
        model_pk = get_model_options(model).pk.name
        is_pk = pk_field == 'pk' or pk_field == model_pk
        if not is_pk:
            dic.update(is_pk=False)
        if is_pk:
            dic.update(pk=pk)
            dic[model_pk] = pk
        else:
            dic[pk_field] = pk
        super().__init__()

    def with_queryset(self, model_or_queryset=None):
        if model_or_queryset is not None:
            assert get_model(model_or_queryset) == self._model
        return self._with_queryset_unsafe(model_or_queryset)

    def _with_queryset_unsafe(self, model_or_queryset=None):
        return type(self)(model_or_queryset or self._model_or_queryset, self._pk, self._pk_field)

    def with_queryset_update(self, model_or_queryset=None):
        self._model_or_queryset = model_or_queryset or self._model_or_queryset
        return self

    def _setup(self):
        result = self._wrapped = get_object_or_404(self._model_or_queryset, Q((self._pk_field, self._pk)))
        return result