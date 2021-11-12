# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from typing import List, Tuple, Union

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ..matrix import Mat3d
from ..vector import Vec3d
from . import color


class Shape:
    def __init__(
        self,
        vertices: List[Vec3d],
        origin: Vec3d = Vec3d.point(0, 0, 0),
        color: Union[
            Tuple[int, int, int],
            List[Tuple[int, int, int]]
        ] = color.WHITE,
        stack=[]
    ):
        self.vertices = vertices
        self.origin = origin
        self.color = color
        self.stack = []
        self._load_stack(stack)

    def draw(self):
        is_multicolored = type(self.color) is list
        color_itr = None

        if is_multicolored:
            color_itr = iter(self.color)
        else:
            glColor3f(self.color[0], self.color[1], self.color[2])

        glBegin(GL_POLYGON)
        for vertice in self.vertices:
            if is_multicolored:
                color = next(color_itr)
                glColor3f(*color)

            position = vertice + self.origin
            glVertex3f(position.x, position.y, position.z)
        glEnd()

    def draw_border(self):
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glColor3f(*color.RED)

        for vertice in self.vertices:
            position = vertice + self.origin
            glVertex3f(position.x, position.y, position.z)
        glEnd()

    def __getitem__(self, index: Union[int, slice]):
        return self.vertices.__getitem__(index)

    def rotate(self, theta_0: float, theta_1: float, theta_2: float, order="xyz") -> None:
        R0 = getattr(Mat3d, f'rotation_{order[0]}_matrix')(theta_0)
        R1 = getattr(Mat3d, f'rotation_{order[1]}_matrix')(theta_1)
        R2 = getattr(Mat3d, f'rotation_{order[2]}_matrix')(theta_2)

        self.vertices = [R2 @ R1 @ R0 @ vertice for vertice in self.vertices]

        self.stack.append(('R', order, theta_0, theta_1, theta_2))

    def translate(self, tx: float, ty: float, tz: float) -> None:
        T = Mat3d.translation_matrix(tx, ty, tz)
        self.vertices = [T @ vertice for vertice in self.vertices]

        self.stack.append(('T', tx, ty, tz))

    def scale(self, sx: float, sy: float, sz: float) -> None:
        S = Mat3d.scaling_matrix(sx, sy, sz)
        self.vertices = [S @ vertice for vertice in self.vertices]

        self.stack.append(('S', sx, sy, sz))

    def undo(self):
        if len(self.stack) == 0:
            return

        transformation = self.stack.pop()

        if transformation[0] == 'S':
            sx = 1 / transformation[1]
            sy = 1 / transformation[2]
            sz = 1 / transformation[3]
            self.scale(sx, sy, sz)
        elif transformation[0] == 'T':
            tx = -transformation[1]
            ty = -transformation[2]
            tz = -transformation[3]
            self.translate(tx, ty, tz)
        elif transformation[0] == 'R':
            order = transformation[1][::-1]
            theta_1 = -transformation[4]
            theta_2 = -transformation[3]
            theta_3 = -transformation[2]
            self.rotate(theta_1, theta_2, theta_3, order)
        else:
            self.stack.append(transformation)
            return

        self.stack.pop()

    def _load_stack(self, stack):
        for transformation in stack:
            if transformation[0] == 'S':
                sx = transformation[1]
                sy = transformation[2]
                sz = transformation[3]
                self.scale(sx, sy, sz)
            elif transformation[0] == 'T':
                tx = transformation[1]
                ty = transformation[2]
                tz = transformation[3]
                self.translate(tx, ty, tz)
            elif transformation[0] == 'R':
                order = transformation[1]
                theta_1 = transformation[4]
                theta_2 = transformation[3]
                theta_3 = transformation[2]
                self.rotate(theta_1, theta_2, theta_3, order)

    def clone(self) -> 'Shape':
        cloned = Shape(
            self.vertices[::], self.origin.clone(), self.color[::])
        cloned.stack = self.stack[::]

        return cloned

    def __str__(self) -> str:
        return self.__class__.__name__ + "(vertices=[" + ", ".join(map(str, self.vertices)) + "])"

    @staticmethod
    def quadrilateral(
        vertice1=Vec3d,
        vertice2=Vec3d,
        vertice3=Vec3d,
        vertice4=Vec3d,
        origin: Vec3d = Vec3d.point(0, 0, 0),
        color: Tuple[int, int, int] = None,
        color1: Tuple[int, int, int] = color.WHITE,
        color2: Tuple[int, int, int] = color.WHITE,
        color3: Tuple[int, int, int] = color.WHITE,
        color4: Tuple[int, int, int] = color.WHITE,
        stack=[]
    ):
        return Shape([vertice1, vertice2, vertice3, vertice4],
                     origin, color or [color1, color2, color3, color4], stack)

    @staticmethod
    def triangle(
        vertice1=Vec3d,
        vertice2=Vec3d,
        vertice3=Vec3d,
        origin: Vec3d = Vec3d.point(0, 0, 0),
        color: Tuple[int, int, int] = None,
        color1: Tuple[int, int, int] = color.WHITE,
        color2: Tuple[int, int, int] = color.WHITE,
        color3: Tuple[int, int, int] = color.WHITE,
        stack=[]
    ):
        return Shape([vertice1, vertice2, vertice3],
                     origin, color or [color1, color2, color3], stack)
