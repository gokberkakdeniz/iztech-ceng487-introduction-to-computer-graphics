# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from ..math import Vec3d
from .color import RGBA
from .shader import Resource

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class BlinToggler(Resource):
    def __init__(self, enabled=False) -> None:
        super().__init__()
        self.enabled = enabled

    def toggle(self):
        self.enabled = not self.enabled

    def load(self):
        glUseProgram(self.program.id)

        blinEnabled = glGetUniformLocation(self.program.id, "blinEnabled")
        glUniform1i(blinEnabled, int(self.enabled))

        glUseProgram(0)


class Light(Resource):
    def __init__(self, intensity: float) -> None:
        super().__init__()
        self.intensity = intensity
        self.__intensity_prev = None

    def is_open(self):
        return self.__intensity_prev is None

    def on(self):
        if self.is_open():
            return

        self.intensity = self.__intensity_prev
        self.__intensity_prev = None

    def off(self):
        if not self.is_open():
            return

        self.__intensity_prev = self.intensity
        self.intensity = 0.0

    def toogle(self):
        if self.__intensity_prev is None:
            self.off()
        else:
            self.on()


class DirectionalLight(Light):
    def __init__(self, direction: Vec3d, color: RGBA, intensity: float = 1.0) -> None:
        super().__init__(intensity)

        self.direction = -direction
        self.color = color

    def set_direction(self, direction):
        self.direction = -direction

    def load(self):
        glUseProgram(self.program.id)

        lightDir = glGetUniformLocation(self.program.id, "dirLight1Dir")
        glUniform3f(lightDir, *self.direction.to_list()[:3])

        lightColor = glGetUniformLocation(self.program.id, "dirLight1Color")
        glUniform4f(lightColor, *self.color.to_list())

        lightIntensity = glGetUniformLocation(self.program.id, "dirLight1Intensity")
        glUniform1f(lightIntensity, self.intensity)

        glUseProgram(0)


class PointLight(Light):
    def __init__(self, position: Vec3d, color: RGBA, intensity: float = 1.0) -> None:
        super().__init__(intensity)

        self.position = position
        self.color = color

    def load(self):
        glUseProgram(self.program.id)

        lightPos = glGetUniformLocation(self.program.id, "pointLight1Pos")
        glUniform3f(lightPos, *self.position.to_list()[:3])

        lightColor = glGetUniformLocation(self.program.id, "pointLight1Color")
        glUniform4f(lightColor, *self.color.to_list())

        lightIntensity = glGetUniformLocation(self.program.id, "pointLight1Intensity")
        glUniform1f(lightIntensity, self.intensity)

        glUseProgram(0)
