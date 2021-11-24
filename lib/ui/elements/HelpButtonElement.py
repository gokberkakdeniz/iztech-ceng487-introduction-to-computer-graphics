# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ..element import Element


class HelpButtonElement(Element):
    def __init__(self) -> None:
        super().__init__()

    def draw(self):
        glColor3f(0.0, 1.0, 1.0)
        glRasterPos2i(3, 2)
        glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'?')

    def draw_border(self):
        pass
