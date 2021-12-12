from itertools import tee


def pairwise(iterable):
    """pairwise('ABCDEFG') --> AB BC CD DE EF FG

    source: https://docs.python.org/3/library/itertools.html#itertools.pairwise"""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
