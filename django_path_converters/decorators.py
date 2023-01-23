from functools import wraps

def require_querydict(**kwargs):
    def wrapper(func):
        @wraps(f)
        def wrapped(request, *args, **kwargs):
            return func(*args, **kwargs)
        return func
    return wrapper
