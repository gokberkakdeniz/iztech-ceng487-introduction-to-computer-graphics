# CENG 487 Assignment5 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ..element import Element


class StatisticsElement(Element):
    def __init__(self) -> None:
        super().__init__()
        self.level = 0
        self.pos = (20, 20)

    def set_level(self, level: int):
        self.level = level

    def set_vertice_count(self, vertice_count: int):
        self.vertice_count = vertice_count

    def set_face_count(self, face_count: int):
        self.face_count = face_count

    def draw(self, background=None, border=None):
        glColor3f(0.0, 1.0, 1.0)
        glWindowPos2f(*self.pos)
        glutBitmapString(GLUT_BITMAP_9_BY_15,
                         (f"Level: {self.level} | Vertice count: {self.vertice_count} | Face count: {self.face_count}").encode("utf-8"))
