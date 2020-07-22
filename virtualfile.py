def open(file, *args, **kwargs):
    if isinstance(file, VertualFile) : return file
    return __builtins__["open"](file, *args, **kwargs)


class VertualFile():
    open = open
    def __init__(self, method="t", doclose=True):
        self.method = list(method)
        self.data = b'' if "b" in self.method else ""
        self.closed = False
        self.doclose = doclose

    def __repr__(self):
        return "%s.VertualFile('%s', %s)"%(__name__, "".join(self.method), self.doclose)

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def check(function):
        def func(self, *args, **kwargs):
            if not self.doclose:
                return function(self, *args, **kwargs)
            if self.closed:
                raise ValueError("I/O operation on closed file.")
            return function(self, *args, **kwargs)
        return func

    @check
    def close(self):
        self.closed = True

    @check
    def truncate(self):
        self.data = b'' if "b" in self.method else ""

    @check
    def read(self):
        return self.data

    @check
    def write(self, data):
        self.data = self.data + data
