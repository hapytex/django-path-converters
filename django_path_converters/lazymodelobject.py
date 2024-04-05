from django.db.models import Model, QuerySet, Manager, Q
from django.db.models.base import ModelState
from django.db.models.options import Options
from django.shortcuts import get_object_or_404
from django.utils.functional import LazyObject, empty

from django_path_converters.utils import get_model_options, get_model, get_queryset, get_model_or_queryset


class BatchLoaderManager:
    # can be used if a queryset uses a different database instead, to move if to a different "bucket"
    def __init__(self):
        self.loaders = {}

    def __getitem__(self, db):
        loader = self.loaders.get(db)
        if loader is None:
            loader = self.loaders[db] = BatchLoader(self, db)
        return loader

    def __setitem__(self, db, item):
        loader = self.loaders.get(db)
        if loader is None:
            self.loaders[db] = item
        else:
            loader.add(*item.items)


class BatchLoader:
    def __init__(self, manager, db, *items):
        self.manager = manager
        self._db = db
        self._items = {id(item): item for item in items}

    @property
    def items(self):
        return self._items.values()

    def add(self, *values):
        for value in values:
            self._items[id(value)] = value

    def migrate(self, *values):
        _values = self._values
        _db = self._db
        for value in values:
            pass

    def _load(self):
        db = None
        for item in self._items.values():
            # possible that these are already fetched
            # we don't do forked querysets, since we assume that
            # was for good reasons
            if item._wrapped is not empty and not item._forked:
                pass


class ModelLazyStateObject(LazyObject):
    def __init__(self, parent):
        self.__dict__.update(_parent=parent)
        super().__init__()

    __class__ = ModelState
    adding = False

    @property
    def db(self):
        return get_queryset(self._parent._model_or_queryset).db

    def _setup(self):
        # we can't use `self.parent._state`, since that will point us back to self
        result = self._parent._wrapped
        if result is empty:  # still to evaluate
            result = self._parent._setup()
        result = self._wrapped = result._state
        return result


class ModelLazyObject(LazyObject):
    # set class fields, to avoid infinite loops when setting attributes
    _pk_field = 'pk'
    _pk = None
    _model_or_queryset = None
    _model = None
    _is_pk = True
    _forked = False
    _batcher = None

    @property
    def __class__(self):
        # used for the isinstance check, this prevents us from querying
        # when performing isinstance functions
        return self._model

    def __dir__(self):
        wrapped = self._wrapped
        # create model instance to get the __dir__
        if self._wrapped is empty:
            return dir(self._model())
        else:
            return dir(wrapped)

    def __init__(self, model_or_queryset, pk, pk_field='pk', check_field=True, batcher=None):
        assert isinstance(model_or_queryset, (type(Model), Model, Options, Manager, QuerySet))
        # prevent loading the object by using a setter
        dic = self.__dict__
        model_or_queryset = get_model_or_queryset(model_or_queryset)
        model = get_model(model_or_queryset)
        dic.update(_model_or_queryset=model_or_queryset, _pk=pk, _model=model)
        # prevent adding attributes to instances
        if pk_field != 'pk':
            dic.update(_pk_field=pk_field)
        if check_field:
            # check if the model indeed *can* resolve the field, will *NOT* make a query
            get_queryset(model_or_queryset).filter(Q((pk_field, pk)))
        model_pk = get_model_options(model).pk.name
        is_pk = pk_field == 'pk' or pk_field == model_pk
        if not is_pk:
            dic.update(_is_pk=False)
        if is_pk:
            dic.update(pk=pk)
            dic[model_pk] = pk
        else:
            dic[pk_field] = pk
        if batcher is not None:
            dic.update(_batcher=batcher)
        super().__init__()

    def with_queryset(self, model_or_queryset=None):
        if model_or_queryset is not None:
            assert get_model(model_or_queryset) == self._model
        result = self._with_queryset_unsafe(model_or_queryset)
        self.__dict__.update(_forked=True)
        return result

    def _with_queryset_unsafe(self, model_or_queryset=None):
        return type(self)(model_or_queryset or self._model_or_queryset, self._pk, self._pk_field, batcher=self._batcher)

    def with_queryset_update(self, model_or_queryset=None):
        self._model_or_queryset = model_or_queryset or self._model_or_queryset
        return self

    @property
    def _state(self):
        return ModelLazyStateObject(self)

    def __bool__(self):
        return True

    def _setup(self):
        result = self._wrapped = get_object_or_404(self._model_or_queryset, Q((self._pk_field, self._pk)))
        return result