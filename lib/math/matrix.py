# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from typing import Union
from math import sin, cos
from ..utils import ensure
from .vector import Vec3d


class Mat3d:
    """
    4x4 row-ordered matrix

    ```
    Mat3d = [Vec3d([x1 y1 z1 w1])
             Vec3d([x2 y2 z2 w2])
             Vec3d([x3 y3 z3 w3])
             Vec3d([x4 y4 z4 w4])]
    ```
    """

    def __init__(self, r1: Vec3d, r2: Vec3d, r3: Vec3d, r4: Vec3d) -> 'Mat3d':
        ensure.type_of(r1, "r1", [Vec3d])
        ensure.type_of(r2, "r2", [Vec3d])
        ensure.type_of(r3, "r3", [Vec3d])
        ensure.type_of(r4, "r4", [Vec3d])

        self.matrix = [r1, r2, r3, r4]

    def to_array(self):
        return [self.matrix[j][i] for i in range(len(self.matrix)) for j in range(4)]

    @staticmethod
    def translation_matrix(tx: float, ty: float, tz: float) -> 'Mat3d':
        return Mat3d(Vec3d(1, 0, 0, tx),
                     Vec3d(0, 1, 0, ty),
                     Vec3d(0, 0, 1, tz),
                     Vec3d(0, 0, 0, 1))

    @staticmethod
    def scaling_matrix(sx: float, sy: float, sz: float) -> 'Mat3d':
        return Mat3d(Vec3d(sx, 0, 0, 0),
                     Vec3d(0, sy, 0, 0),
                     Vec3d(0, 0, sz, 0),
                     Vec3d(0, 0, 0, 1),)

    @staticmethod
    def rotation_matrix(theta_0: float, theta_1: float, theta_2: float, order="xyz") -> 'Mat3d':
        R = None

        if theta_0 != 0:
            R = getattr(Mat3d, f'rotation_{order[0]}_matrix')(theta_0)

        if theta_1 != 0:
            R1 = getattr(Mat3d, f'rotation_{order[1]}_matrix')(theta_1)
            R = R1 if R is None else R1 @ R

        if theta_2 != 0:
            R2 = getattr(Mat3d, f'rotation_{order[2]}_matrix')(theta_2)
            R = R2 if R is None else R2 @ R

        return R or Mat3d.identity()

    @staticmethod
    def rotation_x_matrix(theta: float) -> 'Mat3d':
        return Mat3d(Vec3d(1, 0, 0, 0),
                     Vec3d(0, cos(theta), -sin(theta), 0),
                     Vec3d(0, sin(theta), cos(theta), 0),
                     Vec3d(0, 0, 0, 1))

    @staticmethod
    def rotation_y_matrix(theta: float) -> 'Mat3d':
        return Mat3d(Vec3d(cos(theta), 0, sin(theta), 0),
                     Vec3d(0, 1, 0, 0),
                     Vec3d(-sin(theta), 0, cos(theta), 0),
                     Vec3d(0, 0, 0, 1))

    @staticmethod
    def rotation_z_matrix(theta: float) -> 'Mat3d':
        return Mat3d(Vec3d(cos(theta), -sin(theta), 0, 0),
                     Vec3d(sin(theta), cos(theta), 0, 0),
                     Vec3d(0, 0, 1, 0),
                     Vec3d(0, 0, 0, 1))

    @staticmethod
    def identity():
        return Mat3d(Vec3d(1, 0, 0, 0),
                     Vec3d(0, 1, 0, 0),
                     Vec3d(0, 0, 1, 0),
                     Vec3d(0, 0, 0, 1))

    @staticmethod
    def zero():
        return Mat3d(Vec3d(0, 0, 0, 0),
                     Vec3d(0, 0, 0, 0),
                     Vec3d(0, 0, 0, 0),
                     Vec3d(0, 0, 0, 0))

    def clone(self) -> 'Mat3d':
        return Mat3d(self.matrix[0].clone(),
                     self.matrix[1].clone(),
                     self.matrix[2].clone(),
                     self.matrix[3].clone())

    def __add__(self, mat2: 'Mat3d') -> 'Mat3d':
        ensure.type_of(mat2, "operand", [Mat3d])

        return Mat3d(self.matrix[0] + mat2.matrix[0],
                     self.matrix[1] + mat2.matrix[1],
                     self.matrix[2] + mat2.matrix[2],
                     self.matrix[3] + mat2.matrix[3])

    def __radd__(self, mat2: 'Mat3d') -> 'Mat3d':
        return self + mat2

    def __sub__(self, mat2: 'Mat3d') -> 'Mat3d':
        ensure.type_of(mat2, "operand", [Mat3d])

        return self + (-mat2)

    def __rsub__(self, mat2: 'Mat3d') -> 'Mat3d':
        return self - mat2

    def __mul__(self, scalar: Union[int, float]) -> 'Mat3d':
        ensure.number(scalar, "operand")

        return Mat3d(self.matrix[0] * scalar,
                     self.matrix[1] * scalar,
                     self.matrix[2] * scalar,
                     self.matrix[3] * scalar)

    def __rmul__(self, scalar: Union[int, float]) -> 'Mat3d':
        return self * scalar

    def __truediv__(self, scalar: Union[int, float]) -> 'Mat3d':
        return self * (1 / scalar)

    def __matmul__(self, mat2: Union['Mat3d', 'Vec3d']) -> 'Mat3d':
        ensure.type_of(mat2, "mat", [Vec3d, Mat3d])

        if type(mat2) is Vec3d:
            return Vec3d(self.matrix[0].dot(mat2),
                         self.matrix[1].dot(mat2),
                         self.matrix[2].dot(mat2),
                         self.matrix[3].dot(mat2))

        mat_T = mat2.transpose()

        return Mat3d(*[Vec3d(*[row.dot(row_T) for row_T in mat_T]) for row in self.matrix])

    def transpose(self) -> 'Mat3d':
        return Mat3d(
            Vec3d(self.matrix[0].x, self.matrix[1].x,
                  self.matrix[2].x, self.matrix[3].x),
            Vec3d(self.matrix[0].y, self.matrix[1].y,
                  self.matrix[2].y, self.matrix[3].y),
            Vec3d(self.matrix[0].z, self.matrix[1].z,
                  self.matrix[2].z, self.matrix[3].z),
            Vec3d(self.matrix[0].w, self.matrix[1].w,
                  self.matrix[2].w, self.matrix[3].w)
        )

    def __eq__(self, o: object) -> bool:
        return type(o) and type(self) and \
            self.matrix[0] == o.matrix[0] and \
            self.matrix[1] == o.matrix[1] and \
            self.matrix[2] == o.matrix[2] and \
            self.matrix[3] == o.matrix[3]

    def __getitem__(self, index: int) -> Vec3d:
        return self.matrix[index]

    def __setitem__(self, index: int, value: Vec3d) -> None:
        self.matrix[index] = value

    def __neg__(self) -> 'Mat3d':
        return -1 * self

    def __pos__(self) -> 'Mat3d':
        return self.clone()

    def __str__(self) -> str:
        return "Mat3d(" + ",\n      ".join(map(str, self.matrix)) + ")"
