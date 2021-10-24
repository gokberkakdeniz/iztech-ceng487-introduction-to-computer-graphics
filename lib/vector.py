# CENG 487 Assignment1 by
# Gokberk Akdeniz
# StudentId: 250201041
# 10 2021

from math import acos, pi, sqrt
from typing import Union
from . import ensure


class Vec3d:
    """
    ```
    Vec3d = [x
             y
             z
             w]
    ```
    """

    def __init__(self, x: float, y: float, z: float, w: int):
        ensure.number(x, "x")
        ensure.number(y, "y")
        ensure.number(y, "z")
        ensure.number(w, "w")

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)
        self.order = ["x", "y", "z", "w"]

    @staticmethod
    def point(x, y, z):
        return Vec3d(x, y, z, 1)

    @staticmethod
    def vector(x, y, z):
        return Vec3d(x, y, z, 0)

    def clone(self):
        return Vec3d(self.x, self.y, self.z, self.w)

    def to_point(self):
        return Vec3d(self.x, self.y, self.z, 1)

    def to_vector(self):
        return Vec3d(self.x, self.y, self.z, 0)

    def __str__(self) -> str:
        return "vec3d({}, {}, {}, {})".format(self.x, self.y, self.z, self.w)

    def is_point(self):
        return self.w == 1

    def is_vector(self):
        return self.w == 0

    def cast_to_point(self):
        self.w = 1

    def cast_to_vector(self):
        self.w = 0

    def dot(self, o):
        ensure.type_of(o, "operand", [Vec3d])

        return self.x * o.x + self.y * o.y + self.z * o.z + self.w * o.w

    def cross(self, vec2):
        ensure.type_of(vec2, "operand", [Vec3d])
        if self.w != vec2.w != 0:
            raise TypeError("expected vector not point")

        return Vec3d(self.y * vec2.z - self.z * vec2.y,
                     self.z * vec2.x - self.x * vec2.z,
                     self.x * vec2.y - self.y * vec2.x,
                     0)

    def project(self, vec2):
        return None

    def angle(self, o, degree=False):
        ensure.type_of(o, "operand", [Vec3d])

        radian = acos(self.dot(o) / (self.length() * o.length()))

        return radian * (180 / pi) if degree else radian

    def length(self) -> float:
        return sqrt(self.dot(self))

    def normalize(self):
        return self / self.length()

    def __add__(self, o: object):
        ensure.type_of(o, "operand", [Vec3d])

        return Vec3d(o.x + self.x, o.y + self.y, o.z + self.z, o.w + self.w)

    def __radd__(self, o: object):
        return o + self

    def __sub__(self, o: object):
        ensure.type_of(o, "operand", [Vec3d])

        return self + (-o)

    def __rsub__(self, o: object):
        return o - self

    def __neg__(self):
        return -1 * self

    def __pos__(self):
        return self.clone()

    def __mul__(self, scalar: Union[int, float]):
        ensure.number(scalar, "operand")

        return Vec3d(scalar * self.x, scalar * self.y, scalar * self.z, scalar * self.w)

    def __rmul__(self, scalar: Union[int, float]):
        return self * scalar

    def __truediv__(self, scalar):
        return Vec3d(self.x / scalar, self.y / scalar, self.z / scalar, self.w)

    def __floordiv__(self, scalar):
        return Vec3d(self.x // scalar, self.y // scalar, self.z // scalar, self.w)

    def __eq__(self, o: object) -> bool:
        return type(self) == type(o) and \
            self.x == o.x and \
            self.y == o.y and \
            self.z == o.z and \
            self.w == o.w

    def __getitem__(self, index):
        return self.__getattribute__(self.order[index])

    def __setitem__(self, index, value):
        self.__setattr__(self.order[index], value)
