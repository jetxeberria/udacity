import functools

def create_profile(given_name, *surnames, **details):
    print(given_name, *surnames)
    for k,v in details.items():
        print(f"{k}: {v}")


def memoize(fn, cacher = None):
    if not cacher:
        cacher = Cacher()
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if cacher.finds_in_cache(args, kwargs, fn):
            output_fn = cacher.found_in_cache[1][1]
            cacher.found_in_cache = None
        else:
            output_fn = fn(*args, **kwargs)
            cacher.save_in_cache(args, kwargs, fn, output_fn)
        return output_fn

    return wrapper

class Cacher():
    def __init__(self):
        self.all_cached= []
        self.found_in_cache = None
    
    def save_in_cache(self, args, kwargs, fn, output_fn):
        self.all_cached += [((args, kwargs), (fn, output_fn))]
        if None in self.all_cached:
            self.all_cached.pop(self.all_cached.index(None))

    def finds_in_cache(self, args, kwargs, fn):
            args_found = (args, kwargs)
            for cach in self.all_cached:
                if cach and self.fn_call_match(cach, args_found, fn):
                    self.found_in_cache = cach
                    return True
            return False

    def fn_call_match(self, cach, args_found, fn):
        if cach[0] == args_found and cach[1][0] == fn:
            return True
