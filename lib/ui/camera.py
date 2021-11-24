# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from OpenGL.GLU import *
from OpenGL.GL import *


class Camera:
    def __init__(self) -> None:
        pass

    def look(self):
        glLoadIdentity()
        gluLookAt(0, 0, 6.0, 0, 0, 0, 0, 1, 1)
