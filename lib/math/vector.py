# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from math import acos, cos, pi, sqrt
from typing import Union
from ..utils import ensure
import numpy as np


class Vec3d:
    """
    ```
    4x1 column vector

    Vec3d = [x
             y
             z
             w]
    ```
    """

    def __init__(self, x: float, y: float, z: float, w: float) -> 'Vec3d':
        ensure.number(x, "x")
        ensure.number(y, "y")
        ensure.number(y, "z")
        ensure.number(w, "w")

        self.__cords = np.array([x, y, z, w], dtype=np.float)

    @property
    def x(self):
        return self.__cords[0]

    @x.setter
    def x(self, value: float):
        self.__cords[0] = value

    @property
    def y(self):
        return self.__cords[1]

    @y.setter
    def y(self, value: float):
        self.__cords[1] = value

    @property
    def z(self):
        return self.__cords[2]

    @z.setter
    def z(self, value: float):
        self.__cords[2] = value

    @property
    def w(self):
        return self.__cords[3]

    @w.setter
    def w(self, value: float):
        self.__cords[3] = value

    def to_array(self):
        return self.__cords

    @staticmethod
    def point(x: float, y: float, z: float) -> 'Vec3d':
        return Vec3d(x, y, z, 1)

    @staticmethod
    def vector(x: float, y: float, z: float) -> 'Vec3d':
        return Vec3d(x, y, z, 0)

    def clone(self) -> 'Vec3d':
        return Vec3d(self.x, self.y, self.z, self.w)

    def to_point(self) -> 'Vec3d':
        return Vec3d(self.x, self.y, self.z, 1)

    def to_vector(self) -> 'Vec3d':
        return Vec3d(self.x, self.y, self.z, 0)

    def __str__(self) -> str:
        return "Vec3d({}, {}, {}, {})".format(self.x, self.y, self.z, self.w)

    def is_point(self) -> bool:
        return self.w == 1

    def is_vector(self) -> bool:
        return self.w == 0

    def cast_to_point(self) -> None:
        self.w = 1

    def cast_to_vector(self) -> None:
        self.w = 0

    def dot(self, vec2: 'Vec3d') -> float:
        ensure.type_of(vec2, "operand", [Vec3d])

        return self.x * vec2.x + self.y * vec2.y + self.z * vec2.z + self.w * vec2.w

    def cross(self, vec2: 'Vec3d') -> 'Vec3d':
        ensure.type_of(vec2, "operand", [Vec3d])

        if self.w != vec2.w != 0:
            raise TypeError("expected vector not point")

        return Vec3d(self.y * vec2.z - self.z * vec2.y,
                     self.z * vec2.x - self.x * vec2.z,
                     self.x * vec2.y - self.y * vec2.x,
                     0)

    def project(self, vec2: 'Vec3d') -> 'Vec3d':
        return self.length() * cos(self.angle(vec2)) * vec2.normalize()

    def angle(self, vec2: 'Vec3d', degree: bool = False) -> float:
        ensure.type_of(vec2, "operand", [Vec3d])

        radian = acos(self.dot(vec2) / (self.length() * vec2.length()))

        return radian * (180 / pi) if degree else radian

    def length(self) -> float:
        return sqrt(self.dot(self))

    def normalize(self) -> 'Vec3d':
        return self / self.length()

    def __add__(self, vec2: 'Vec3d') -> 'Vec3d':
        ensure.type_of(vec2, "operand", [Vec3d])

        return Vec3d(vec2.x + self.x, vec2.y + self.y, vec2.z + self.z, vec2.w + self.w)

    def __radd__(self, vec2: 'Vec3d') -> 'Vec3d':
        return vec2 + self

    def __sub__(self, vec2: 'Vec3d') -> 'Vec3d':
        ensure.type_of(vec2, "operand", [Vec3d])

        return self + (-vec2)

    def __rsub__(self, o: object) -> 'Vec3d':
        return o - self

    def __neg__(self) -> 'Vec3d':
        return -1 * self

    def __pos__(self) -> 'Vec3d':
        return self.clone()

    def __mul__(self, scalar: Union[int, float]) -> 'Vec3d':
        ensure.number(scalar, "operand")

        return Vec3d(scalar * self.x, scalar * self.y, scalar * self.z, scalar * self.w)

    def __rmul__(self, scalar: Union[int, float]) -> 'Vec3d':
        return self * scalar

    def __truediv__(self, scalar: Union[int, float]) -> 'Vec3d':
        return Vec3d(self.x / scalar, self.y / scalar, self.z / scalar, self.w / scalar)

    def __floordiv__(self, scalar: Union[int, float]) -> 'Vec3d':
        return Vec3d(self.x // scalar, self.y // scalar, self.z // scalar, self.w / scalar)

    def __eq__(self, o: object) -> bool:
        return type(self) == type(o) and \
            self.x == o.x and \
            self.y == o.y and \
            self.z == o.z and \
            self.w == o.w

    def __abs__(self):
        return Vec3d(abs(self.x), abs(self.y), abs(self.z), abs(self.w))

    def __round__(self, ndigits=None):
        return Vec3d(round(self.x, ndigits), round(self.y, ndigits), round(self.z, ndigits), round(self.w, ndigits))

    def __getitem__(self, index: Union[int, slice]) -> float:
        return self.__cords[index]

    def __setitem__(self, index: int, value: float) -> None:
        self.__cords[index] = value

    def __hash__(self) -> int:
        return hash(tuple(self.__cords))
