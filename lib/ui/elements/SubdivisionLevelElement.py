# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ..element import Element


class SubdivisionLevelElement(Element):
    def __init__(self) -> None:
        super().__init__()
        self.level = ""

    def set_level(self, level: str):
        self.level = level

    def draw(self):
        glColor3f(0.0, 1.0, 1.0)
        glRasterPos2i(-3, -2)
        glutBitmapString(GLUT_BITMAP_9_BY_15,
                         self.level.encode("utf-8"))

    def draw_border(self):
        pass
