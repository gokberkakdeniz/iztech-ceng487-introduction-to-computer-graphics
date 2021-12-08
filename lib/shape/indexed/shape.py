# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import List, Tuple, Union

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ..shape import Shape

from ...math import Vec3d, Mat3d

from .. import color


class IndexedShape(Shape):
    def __init__(
        self,
        vertices: List[Vec3d],
        color: Union[
            Tuple[int, int, int],
            List[Tuple[int, int, int]]
        ] = color.WHITE,
        state=(None, None)
    ):
        self.vertices = vertices
        self.color = color
        self.stack = (state[0] or []).copy()
        self.matrix = state[1] or Mat3d.identity()

        if state[0] is not None:
            self.vertices = [self.matrix @
                             vertice for vertice in self.vertices]

    def draw(self, border=True, background=True):
        is_multicolored = type(self.color) is list
        color_itr = None

        if is_multicolored:
            color_itr = iter(self.color)
        else:
            glColor3f(self.color[0], self.color[1], self.color[2])

        glBegin(GL_POLYGON)
        for vertice in self.vertices:
            if border:
                glLineWidth(2)
                glBegin(GL_LINE_LOOP)
                glColor3f(*color.RED)
                glVertex3f(vertice.x, vertice.y, vertice.z)
                glEnd()

            if is_multicolored:
                color = next(color_itr)
                glColor3f(*color)

                glVertex3f(vertice.x, vertice.y, vertice.z)
        glEnd()

    def __getitem__(self, index: Union[int, slice]):
        return self.vertices.__getitem__(index)

    def rotate(self, theta_0: float, theta_1: float, theta_2: float, order="xyz") -> None:
        R = Mat3d.rotation_matrix(theta_0, theta_1, theta_2, order)
        self.matrix = R @ self.matrix

        self.vertices = [R @ vertice for vertice in self.vertices]

        self.stack.append(('R', order, theta_0, theta_1, theta_2))

    def translate(self, tx: float, ty: float, tz: float) -> None:
        T = Mat3d.translation_matrix(tx, ty, tz)
        self.matrix = T @ self.matrix

        self.vertices = [T @ vertice for vertice in self.vertices]

        self.stack.append(('T', tx, ty, tz))

    def scale(self, sx: float, sy: float, sz: float) -> None:
        S = Mat3d.scaling_matrix(sx, sy, sz)
        self.matrix = S @ self.matrix

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
        color: Tuple[int, int, int] = None,
        color1: Tuple[int, int, int] = color.WHITE,
        color2: Tuple[int, int, int] = color.WHITE,
        color3: Tuple[int, int, int] = color.WHITE,
        color4: Tuple[int, int, int] = color.WHITE,
        state=(None, None)
    ):
        return Shape([vertice1, vertice2, vertice3, vertice4],
                     color or [color1, color2, color3, color4], state)

    @staticmethod
    def triangle(
        vertice1=Vec3d,
        vertice2=Vec3d,
        vertice3=Vec3d,
        color: Tuple[int, int, int] = None,
        color1: Tuple[int, int, int] = color.WHITE,
        color2: Tuple[int, int, int] = color.WHITE,
        color3: Tuple[int, int, int] = color.WHITE,
        state=(None, None)
    ):
        return Shape([vertice1, vertice2, vertice3],
                     color or [color1, color2, color3], state)
