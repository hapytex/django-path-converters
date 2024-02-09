from functools import wraps
import re

from django.http import Http404
from django.urls.converters import get_converter
from django.utils.datastructures import MultiValueDict
import re

def _get_converter(conv):
    if isinstance(conv, str):
        conv = get_converter(conv)
    return (re.compile(conv.regex), conv.to_python)

def require_querydict(*, _required=(), **kwargs):
    converters = {
        k: _get_converter(v) for k, v in kwargs
    }
    def validate_convert(name, conv, vals):
        if conv is None:
            return vals
        rgx, f = conv
        result = []
        for val in vals:
            if rgx.fullmatch(val):
                result.append(f(val))
            else:
                raise Http404(f'The query parameter ?{name}={val} does not satisfy the required pattern.')
        return result

    def wrapper(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            data = request.GET
            for req in _required:
                if req not in data:
                    raise Http404(f'The query string requires a ?{req}=… parameter.')
            request.GET = MultiValueDict([
                (k, validate_convert(k, converters.get(k), vs))
                for k, vs in request.GET.lists()
            ])
            return func(*args, **kwargs)
        return wrapped
    return wrapper


class RequireQueryStringMixin:
    querystring_required = ()
    querystring_converters = None

    def get_querystring_required(self):
        return self.querystring_required

    def get_querystring_converters(self):
        return self.querystring_converters or {}

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        # todo: rewrite request.GET
