
from typing import Tuple

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ...math import Vec3d
from .shape import WingedEdgeShape


class Grid(WingedEdgeShape):
    def __init__(self,
                 shape: Tuple[int, int],
                 name: str = None):
        super().__init__(name=name)
        self.shape = shape

        size_x, size_z = self.shape

        for xi in range(size_x):
            x = xi - size_x / 2
            for zi in range(size_z):
                z = zi - size_z / 2

                self.add_face([Vec3d.point(x, 0, z),
                               Vec3d.point(x+1, 0, z),
                               Vec3d.point(x+1, 0, z+1),
                               Vec3d.point(x, 0, z+1)], ())

    def draw(self, border=True, background=False) -> None:
        size_x, size_z = self.shape

        size_x = size_x / 2
        size_z = size_z / 2

        glPointSize(4)
        glBegin(GL_POINTS)

        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)

        glEnd()

        glLineWidth(4)
        glBegin(GL_LINES)

        glColor3f(0, 1, 0)
        glVertex3f(-size_x, 0, 0)
        glVertex3f(+size_x, 0, 0)

        glColor3f(0, 0, 1)
        glVertex3f(0, 0, -size_z)
        glVertex3f(0, 0, size_z)

        glEnd()

        super().draw(border=border, background=False)
