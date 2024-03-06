from collections import defaultdict
from django_path_converters.lazymodelobject import ModelLazyObject, BatchLoader, BatchLoaderManager

class QueryBatcherMiddleware:

    def __init__(self, _get_response):
        self._get_response = _get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        batches = defaultdict(list)
        for parameter in (*view_args, *view_kwargs.values()):
            if isinstance(parameter, ModelLazyObject):
                batches[parameter._state.db].append(parameter)
        if batches:
            manager = BatchLoaderManager()
            for db, batch in batches.items():
                batcher = manager[db] = BatchLoader(manager, *batch)
                for item in batch:
                    item.__dict__.update(_batcher=batcher)

    def __call__(self, request):
        return self._get_response(request)
