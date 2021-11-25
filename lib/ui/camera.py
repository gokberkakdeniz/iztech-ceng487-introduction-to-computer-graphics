# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from OpenGL.GLU import *
from OpenGL.GL import *
from ..math import Mat3d


class Camera:
    def __init__(self) -> None:
        self.matrix = Mat3d.translation_matrix(0, 0, -6)

    def zoom_in(self, factor=1.25):
        self.matrix @= Mat3d.scaling_matrix(
            factor, factor, factor
        )

    def zoom_out(self, factor=0.8):
        self.matrix @= Mat3d.scaling_matrix(
            factor, factor, factor
        )

    def rotate(self, x: float, y: float, z: float):
        self.matrix @= Mat3d.rotation_z_matrix(z) \
            @ Mat3d.rotation_y_matrix(y) \
            @ Mat3d.rotation_x_matrix(x)

    def reset(self):
        self.matrix = Mat3d.translation_matrix(0, 0, -6)

    def look(self):
        glLoadMatrixf(self.matrix.to_array())
