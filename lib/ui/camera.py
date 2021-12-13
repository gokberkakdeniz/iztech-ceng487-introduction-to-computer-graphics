# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from OpenGL.GLU import *
from OpenGL.GL import *

from lib.shape.shader import Program
from ..math import Mat3d


class Camera:
    def __init__(self) -> None:
        self.matrix = Mat3d.identity()

    def zoom_in(self, factor=1.25):
        self.matrix @= Mat3d.scaling_matrix(
            factor, factor, factor
        )

    def zoom_out(self, factor=0.8):
        self.matrix @= Mat3d.scaling_matrix(
            factor, factor, factor
        )

    def rotate(self, x: float, y: float, z: float):
        self.matrix @= Mat3d.rotation_matrix(x, y, z)

    def reset(self):
        self.matrix = Mat3d.identity()

    def look(self, program: Program = None):
        if program is None:
            glLoadMatrixf(self.matrix.to_array())
        else:
            glUseProgram(program.id)
            modelLocation = glGetUniformLocation(program.id, "camera")
            glUniformMatrix4fv(modelLocation, 1, GL_FALSE, self.matrix.to_array())
            glUseProgram(0)
