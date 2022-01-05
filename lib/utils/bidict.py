# CENG 487 Assignment7 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import Dict, Generic, TypeVar

L = TypeVar('L')
R = TypeVar('R')


class bidict(Generic[L, R]):
    """
    bidirectional dictionary

    idea: https://stackoverflow.com/a/1456390
    """

    def __init__(self) -> None:
        self.l2r: Dict[L, R] = {}  # left => right
        self.r2l: Dict[R, L] = {}  # right => left

    def has_left(self, left: L) -> bool:
        return left in self.l2r

    def get_left(self, right: R) -> L:
        return self.r2l.get(right)

    def get_right(self, left: L) -> R:
        return self.l2r.get(left)

    def has_right(self, right: R) -> bool:
        return right in self.r2l

    def add(self, left: L, right: R):
        self.l2r[left] = right
        self.r2l[right] = left

    def update_left(self, left: L, right: R):
        del self.l2r[self.r2l[right]]

        self.l2r[left] = right
        self.r2l[right] = left

    def update_right(self, left: L, right: R):
        del self.r2l[self.l2r[left]]

        self.l2r[left] = right
        self.r2l[right] = left

    def delete(self, left: L, right: R):
        del self.l2r[left]
        del self.r2l[right]

    def lefts(self):
        return self.l2r.items()

    def rights(self):
        return self.r2l.items()

    def items(self):
        return self.l2r.items()
