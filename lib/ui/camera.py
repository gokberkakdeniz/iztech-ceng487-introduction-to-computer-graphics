# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from OpenGL.GLU import *
from OpenGL.GL import *


class Camera:
    def __init__(self) -> None:
        self.args = [0, 0, 6.0, 0, 0, 0, 0, 1, 1]

    def set_eye(self, x: float = None, y: float = None, z: float = None):
        self.args[0] = x or self.args[0]
        self.args[1] = y or self.args[1]
        self.args[2] = z or self.args[2]

    def get_eye(self):
        return self.args[0:3]

    def get_eye_x(self):
        return self.args[0]

    def get_eye_y(self):
        return self.args[1]

    def get_eye_z(self):
        return self.args[2]

    def set_center(self, x: float = None, y: float = None, z: float = None):
        self.args[3] = x or self.args[3]
        self.args[4] = y or self.args[4]
        self.args[5] = z or self.args[5]

    def zoom_in(self, factor=1.25):
        self.set_eye(z=self.get_eye_z() / factor)

    def zoom_out(self, factor=1.25):
        self.set_eye(z=self.get_eye_z() * factor)

    def look(self):
        glLoadIdentity()
        gluLookAt(*self.args)
