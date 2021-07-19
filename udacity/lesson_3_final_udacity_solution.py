import functools
import inspect
def check_types(severity=1):
    if severity == 0:
        return lambda function: function

    def message(msg):
        if severity == 1:
            print(msg)
        else:
            raise TypeError(msg)
    def checker(function):
        expected = function.__annotations__

        assert(all(map(lambda exp: isinstance(exp, type), expected.values())))
        if not expected:
            return function
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            bound_arguments = bind_args(function, *args, **kwargs)
            for arg, val in bound_arguments.items():
                if arg not in expected:
                    continue
                if not isinstance(val, expected[arg]):
                    message(f"Bad Argument! Received {arg}={val}, expecting object of type {expected[arg]}")
            retval = function(*args, **kwargs)
            if 'return' in expected and not isinstance(retval, expected['return']):
                message(f"Bad Return Value! Received {retval}, but expected value of type {expected['return']}")
            return retval
        return wrapper
    return checker

def bind_args(signature, *args, **kwargs):
    return inspect.signature(function).bind(*args, **kwargs).arguments
