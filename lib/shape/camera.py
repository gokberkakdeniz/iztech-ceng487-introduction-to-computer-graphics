# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
from lib.math.vector import Vec3d

from lib.shape.shader import Resource
from ..math import Mat3d


class Camera(Resource):
    def __init__(self, aspect: float) -> None:
        super().__init__()
        self.matrix = Mat3d.translation_matrix(0, 0, -6)
        self.fov = 45.0
        self.aspect = aspect or 1
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

    def translate(self, x: float, y: float, z: float):
        self.matrix @= Mat3d.translation_matrix(x, y, z)

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

    def load(self):
        if self.program is None:
            matrix = self.matrix.to_array()
            glLoadMatrixf(matrix)
        else:
            glUseProgram(self.program.id)

            modelLocation = glGetUniformLocation(self.program.id, "model")
            glUniformMatrix4fv(modelLocation, 1, GL_FALSE, Mat3d.identity().to_array())

            viewLocation = glGetUniformLocation(self.program.id, "view")
            glUniformMatrix4fv(viewLocation, 1, GL_FALSE, self.matrix.to_array())

            projection = self.__get_projection_matrix(self.fov, self.aspect, self.near, self.far).to_array()
            projectionLocation = glGetUniformLocation(self.program.id, "projection")
            glUniformMatrix4fv(projectionLocation, 1, GL_FALSE, projection)

            cameraPosLocation = glGetUniformLocation(self.program.id, "cameraPos")
            glUniform3f(cameraPosLocation, 0, 0, 0)

            glUseProgram(0)

    def should_reload(self):
        return True
