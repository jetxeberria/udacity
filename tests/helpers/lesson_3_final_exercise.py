import inspect

from udacity import lesson_3_final_exercise as l3

def bind_args(function, *args, **kwargs):
    return inspect.signature(function).bind(*args, **kwargs).arguments

@l3.check_types(severity=2)
def foo(a: int, b: str) -> bool:
    return b[a] == 'X'
