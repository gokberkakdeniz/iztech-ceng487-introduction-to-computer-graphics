# CENG 487 Assignment1 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from typing import List, Tuple, Union
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from lib.matrix import Mat3d
from lib.vector import Vec3d
import lib.color as color
origin_zero = Vec3d.point(0, 0, 0)
color_white = (1, 1, 1)


class Shape:
    def __init__(
        self,
        vertices: List[Vec3d],
        origin: Vec3d = origin_zero,
        color: Union[Tuple[int, int, int],
                     List[Tuple[int, int, int]]] = color_white
    ):
        self.vertices = vertices
        self.origin = origin
        self.color = color
        self.stack = []

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

    def transform(self, T: Mat3d):
        self.stack.append(T)
        # print("ONCE", *self.vertices)
        self.vertices = [T @ vertice for vertice in self.vertices]
        # print("SONRA", *self.vertices)

    def undo(self):
        inv_T = self.stack.pop()  # .inverse()
        pass

    def clone(self):
        cloned = Shape(
            self.vertices[::], self.origin.clone(), self.color[::])
        cloned.stack = self.stack[::]

        return cloned

    def __str__(self) -> str:
        return self.__class__.__name__ + "(" + ", ".join(map(str, self.vertices)) + ")"

    @staticmethod
    def quadrilateral(
        vertice1=Vec3d,
        vertice2=Vec3d,
        vertice3=Vec3d,
        vertice4=Vec3d,
        origin: Vec3d = origin_zero,
        color: Tuple[int, int, int] = None,
        color1: Tuple[int, int, int] = color_white,
        color2: Tuple[int, int, int] = color_white,
        color3: Tuple[int, int, int] = color_white,
        color4: Tuple[int, int, int] = color_white,
    ):
        return Shape([vertice1, vertice2, vertice3, vertice4],
                     origin, color or [color1, color2, color3, color4])

    @staticmethod
    def triangle(
        vertice1=Vec3d,
        vertice2=Vec3d,
        vertice3=Vec3d,
        origin: Vec3d = origin_zero,
        color: Tuple[int, int, int] = None,
        color1: Tuple[int, int, int] = color_white,
        color2: Tuple[int, int, int] = color_white,
        color3: Tuple[int, int, int] = color_white,
    ):
        return Shape([vertice1, vertice2, vertice3],
                     origin, color or [color1, color2, color3])
