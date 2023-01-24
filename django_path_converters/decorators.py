from functools import wraps

def require_querydict(**kwargs):
    def wrapper(func):
        @wraps(f)
        def wrapped(request, *args, **kwargs):
            request.GET = MultiValueDict(
                for k, vs in request.GET.lists()
            ]
            return func(*args, **kwargs)
        return func
    return wrapper
