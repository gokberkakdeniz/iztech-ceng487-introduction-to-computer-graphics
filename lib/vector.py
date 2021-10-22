# CENG 487 Assignment1 by
# Gokberk Akdeniz
# StudentId: 250201041
# 10 2021

from math import acos, pi, sqrt
from typing import Union
from . import ensure


class vec3d:
    def __init__(self, x: float, y: float, z: float, w: int):
        ensure.number(x, "x")
        ensure.number(y, "y")
        ensure.number(y, "z")
        ensure.one_of(w, "w", [0, 1])

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.__w = w

    @classmethod
    def point(cls, x, y, z):
        return cls(x, y, z, 1)

    @classmethod
    def vector(cls, x, y, z):
        return cls(x, y, z, 0)

    def clone(self):
        return vec3d(self.x, self.y, self.z, self.__w)

    def to_point(self):
        return vec3d(self.x, self.y, self.z, 1)

    def to_vector(self):
        return vec3d(self.x, self.y, self.z, 0)

    def __str__(self) -> str:
        return "{}({}, {}, {})".format("P" if self.__w else "V", self.x, self.y, self.z)

    def is_point(self):
        return self.__w == 1

    def is_vector(self):
        return self.__w == 0

    def cast_to_point(self):
        self.__w = 1

    def cast_to_vector(self):
        self.__w = 0

    def dot(self, o):
        ensure.type_of(o, "operand", [vec3d])

        return self.x * o.x + self.y * o.y + self.z * o.z + self.__w * o.__w

    def cross(self, vec2):
        return None

    def project(self, vec2):
        return None

    def angle(self, o, degree=False):
        ensure.type_of(o, "operand", [vec3d])

        radian = acos(self.dot(o) / (self.length() * o.length()))

        return radian * (180 / pi) if degree else radian

    def length(self) -> float:
        return sqrt(self.dot(self))

    def normalize(self):
        return self / self.length()

    def __add__(self, o: object):
        ensure.type_of(o, "operand", [vec3d])

        if self.__w != o.__w:
            raise TypeError("'w's are not same.")

        return vec3d(o.x + self.x, o.y + self.y, o.z + self.z, self.__w)

    def __radd__(self, o: object):
        return o + self

    def __sub__(self, o: object):
        ensure.type_of(o, "operand", [vec3d])

        if self.__w != o.__w:
            raise TypeError("'w's are not same.")

        return self + (-o)

    def __rsub__(self, o: object):
        return o - self

    def __neg__(self):
        return -1 * self

    def __pos__(self):
        return self.clone()

    def __mul__(self, scalar: Union[int, float]):
        ensure.number(scalar, "operand")

        return vec3d(scalar * self.x, scalar * self.y, scalar * self.z, self.__w)

    def __rmul__(self, scalar: Union[int, float]):
        return self * scalar

    def __truediv__(self, scalar):
        return vec3d(self.x / scalar, self.y / scalar, self.z / scalar, self.__w)

    def __floordiv__(self, scalar):
        return vec3d(self.x // scalar, self.y // scalar, self.z // scalar, self.__w)

    def __eq__(self, o: object) -> bool:
        return type(self) == type(o) and \
            self.x == o.x and \
            self.y == o.y and \
            self.z == o.z and \
            self.__w == o.__w
