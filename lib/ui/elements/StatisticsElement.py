# CENG 487 Assignment6 by
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
        self.ratio = 0
        self.pos = (20, 20)

    def set_ratio(self, level: int):
        self.ratio = level

    def set_light1(self, on: bool):
        self.light1 = on

    def set_light2(self, on: bool):
        self.light2 = on

    def set_light3(self, on: bool):
        self.light3 = on

    def set_blin(self, on: bool):
        self.blin = on

    def set_vertice_count(self, vertice_count: int):
        self.vertice_count = vertice_count

    def set_face_count(self, face_count: int):
        self.face_count = face_count

    def draw(self, background=None, border=None):
        text = " | ".join([
            f'Ratio: {self.ratio:.2f}',
            f'L1: {"on" if self.light1 else "off"}',
            f'L2: {"on" if self.light2 else "off"}',
            f'L3: { "on" if self.light3 else "off"}',
            f'Blin: {"on" if self.blin else "off"}',
        ])
        glColor3f(0.0, 1.0, 1.0)
        glWindowPos2f(*self.pos)
        glutBitmapString(GLUT_BITMAP_9_BY_15, text.encode("utf-8"))
