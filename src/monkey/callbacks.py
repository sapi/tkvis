import inspect
import sys


class Event(object):
    def __init__(self, obj, fn, args, kwargs, result):
        self.obj = obj
        self.fn = fn

        self.args = args
        self.kwargs = kwargs

        self.result = result

    def __str__(self):
        if self.obj is None:
            return '{}(...) -> {}'.format(self.fn.__name__, self.result)

        return '{!r}.{}(...) -> {}'.format(self.obj, self.fn.__name__,
                self.result)


def log(fn, isMethod=True):
    def f(*args, **kwargs):
        result = fn(*args, **kwargs)

        if isMethod:
            self = args[0]
            args = args[1:]
        else:
            self = None

        evt = Event(self, fn, args, kwargs, result)
        print evt

        return result
    return f


def monitor(moduleName):
    module = sys.modules[moduleName]

    functions = inspect.getmembers(module, inspect.isfunction)

    for name,fn in functions:
        setattr(module, name, log(fn, isMethod=False))

    classes = inspect.getmembers(module, inspect.isclass)

    for _,cls in classes:
        methods = inspect.getmembers(cls, inspect.ismethod)

        for name,method in methods:
            setattr(cls, name, log(method, isMethod=True))
