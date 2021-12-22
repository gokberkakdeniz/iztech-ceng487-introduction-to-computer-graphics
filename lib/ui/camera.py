# CENG 487 Assignment5 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
from lib.math.vector import Vec3d

from lib.shape.shader import Program
from ..math import Mat3d


class Camera:
    def __init__(self) -> None:
        self.matrix = Mat3d.translation_matrix(0, 0, -6)
        self.fov = 45.0
        self.aspect = 640/480
        self.near = 0.1
        self.far = 100.0

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
        self.matrix = Mat3d.translation_matrix(0, 0, -6)

    def __get_projection_matrix(self, fov, aspect, near, far):
        f = np.reciprocal(np.tan(np.divide(np.deg2rad(fov), 2.0)))
        base = near - far
        term_0_0 = np.divide(f, aspect)
        term_2_2 = np.divide(far + near, base)
        term_2_3 = np.divide(np.multiply(np.multiply(2, near), far), base)

        # https://en.wikibooks.org/wiki/GLSL_Programming/Vertex_Transformations
        return Mat3d(Vec3d(term_0_0, 0.0, 0.0, 0.0),
                     Vec3d(0.0, f, 0.0, 0.0),
                     Vec3d(0.0, 0.0, term_2_2, term_2_3),
                     Vec3d(0.0, 0.0, -1, 0.0))

    def look(self, program: Program = None):
        if program is None:
            matrix = self.matrix.to_array()
            glLoadMatrixf(matrix)
        else:
            glUseProgram(program.id)
            modelLocation = glGetUniformLocation(program.id, "camera")
            matrix = (self.__get_projection_matrix(self.fov, self.aspect, self.near, self.far) @ self.matrix).to_array()
            glUniformMatrix4fv(modelLocation, 1, GL_FALSE, matrix)
            glUseProgram(0)
