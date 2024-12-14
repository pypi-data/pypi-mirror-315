# coding: utf-8

__all__ = 'stfu', 'stfu_all'


class STFU(object):
    """ Silence chosen exceptions.
        Use the `stfu` instance directly.
    """

    def __init__(self, *args):
        self.cls = args or None

    def __enter__(self):
        return self

    def __call__(self, *args):
        return type(self)(*args)

    def __exit__(self, cls, exc, trace):
        if self.cls is None or cls is None or issubclass(cls, self.cls):
            return True


stfu = STFU(Exception)
stfu_all = STFU()

