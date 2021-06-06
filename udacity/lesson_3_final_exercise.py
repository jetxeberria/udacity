import functools
import inspect

def check_types(severity=1):
    if severity not in [0, 1, 2]:
        raise Exception("severity must be a value within [1,2,3]")
    def checker(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            if severity == 0:
                return function(*args, **kwargs)
            retval = None
            mismatchings = find_mismatchings(function, *args, **kwargs)
            if not mismatchings:
                retval = function(*args, **kwargs)
            output_mismatch = find_out_mismatch(function, retval)
            if output_mismatch:
                mismatchings.append(output_mismatch)
            if mismatchings:
                if severity == 1:
                    [print(mismatch) for mismatch in mismatchings]
                elif severity == 2:
                    raise AnnotationError(mismatchings)
            return function(*args, **kwargs)

        return wrapper
    return checker


def find_mismatchings(function, *args, **kwargs):
    mismatchings = []
    signature = get_signature(function)
    if signature:
        binded = bind_args(signature, *args, **kwargs)
        mismatchings = [find_mismatching(b, signature) for b in binded.items()]
        while None in mismatchings:
            mismatchings.remove(None)
    return mismatchings

def find_out_mismatch(function, retval):
    mismatch = None
    signature = get_signature(function)
    if signature:
        expected = signature.return_annotation
        if expected != type(retval):
            mismatch = f"Output expected of type '{expected}' but provided '{retval}' as '{type(retval)}'"
    return mismatch



def find_mismatching(arg, signature):
    annotation = signature.parameters[arg[0]].annotation
    if not annotation == type(arg[1]):
        return f"Argument '{arg[0]}' expected of type '{annotation}' but provided '{arg[1]}' as '{type(arg[1])}'"

def bind_args(signature, *args, **kwargs):
    return signature.bind(*args, **kwargs).arguments

def get_signature(function):
    try:
        signature = inspect.signature(function)
    except Exception as exc:
        print(exc)
        return None
    return signature 


class AnnotationError(Exception):
    """ Exception raised due to annotation mismatch with supplied arguments. """
    pass
