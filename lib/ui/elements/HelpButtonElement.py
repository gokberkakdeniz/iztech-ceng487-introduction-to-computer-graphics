# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ..element import Element


class HelpButtonElement(Element):
    def __init__(self) -> None:
        super().__init__()
        self.pos = (0, 0)

    def set_pos(self, pos):
        self.pos = pos

    def draw(self, background=None, border=None):
        glColor3f(0.0, 1.0, 1.0)
        glWindowPos2d(*self.pos)
        glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'?')
