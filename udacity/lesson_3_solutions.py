import functools

def memoize(function):
    function._cache = {}
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in function._cache:
            function._cache[key] = function(*args, **kwargs)
        return function._cache[key]
    return wrapper