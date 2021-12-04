# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ..element import Element


class SubdivisionLevelElement(Element):
    def __init__(self) -> None:
        super().__init__()
        self.level = 0

    def set_level(self, level: int):
        self.level = level

    def draw(self):
        glColor3f(0.0, 1.0, 1.0)
        glRasterPos2i(-3, -2)
        glutBitmapString(GLUT_BITMAP_9_BY_15,
                         (f"Level: {self.level}").encode("utf-8"))

    def draw_border(self):
        pass
