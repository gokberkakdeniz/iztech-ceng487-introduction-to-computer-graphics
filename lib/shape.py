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

    def __getitem__(self, index: Union[int, slice]):
        return self.vertices.__getitem__(index)

    def transform(self, T: Mat3d):
        self.stack.append(T)
        self.vertices = [T @ vertice for vertice in self.vertices]

    def undo(self):
        inv_T = self.stack.pop()  # .inverse()
        pass

    def clone(self):
        cloned = Shape(self.vertices, self.origin, self.color)
        cloned.stack = self.stack[::]

        return cloned
