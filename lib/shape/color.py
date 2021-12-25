# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

import numpy as np
from ..utils import ensure

RED = (1.0, 0.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
PINK = (1, 0.0, 0.8)
VIOLET = (0.5, 0.0, 1.0)
CYAN = (0.0, 1.0, 1.0)
GRAY = (0.4, 0.4, 0.4)
WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)


class RGBA:
    def __init__(self, r: float, g: float, b: float, a: float) -> 'RGBA':
        ensure.number(r, "r")
        ensure.number(g, "g")
        ensure.number(b, "b")
        ensure.number(a, "a")

        self.__cords = np.array([r, g, b, a], dtype=np.float)

    @staticmethod
    def red():
        return RGBA(1.0, 0.0, 0.0, 1.0)

    @staticmethod
    def green():
        return RGBA(0.0, 1.0, 0.0, 1.0)

    @staticmethod
    def blue():
        return RGBA(0.0, 0.0, 1.0, 1.0)

    @staticmethod
    def white():
        return RGBA(1.0, 1.0, 1.0, 1.0)

    @staticmethod
    def gray():
        return RGBA(0.4, 0.4, 0.4, 1.0)

    @staticmethod
    def black():
        return RGBA(0.0, 0.0, 0.0, 1.0)

    @property
    def r(self):
        return self.__cords[0]

    @r.setter
    def r(self, value: float):
        self.__cords[0] = value

    @property
    def g(self):
        return self.__cords[1]

    @g.setter
    def g(self, value: float):
        self.__cords[1] = value

    @property
    def b(self):
        return self.__cords[2]

    @b.setter
    def b(self, value: float):
        self.__cords[2] = value

    @property
    def a(self):
        return self.__cords[3]

    @a.setter
    def a(self, value: float):
        self.__cords[3] = value

    def to_array(self):
        return self.__cords

    def to_list(self):
        return self.__cords.tolist()

    def __hash__(self) -> int:
        return self.r * 255 * 10e9 + self.g * 255 * 10e6 + self.b * 255 * 10e3 + self.a * 255
