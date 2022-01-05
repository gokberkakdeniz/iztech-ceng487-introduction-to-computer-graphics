# CENG 487 Assignment7 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from math import cos
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
        self.reload = True

    def toggle(self):
        self.enabled = not self.enabled
        self.reload = True

    def should_reload(self):
        return self.reload

    def load(self):
        glUseProgram(self.program.id)

        blinEnabled = glGetUniformLocation(self.program.id, "blinEnabled")
        glUniform1i(blinEnabled, int(self.enabled))

        glUseProgram(0)

        self.reload = False


class Light(Resource):
    def __init__(self, intensity: float, color: RGBA) -> None:
        super().__init__()
        self.intensity = intensity
        self.color = color
        self.__intensity_prev = None
        self.reload = True

    def set_color(self, color: RGBA):
        self.color = color
        self.reload = True

    def set_intensity(self, intensity: float):
        self.color = intensity
        self.reload = True

    def is_on(self):
        return self.__intensity_prev is None

    def on(self):
        if self.is_on():
            return

        self.intensity = self.__intensity_prev
        self.__intensity_prev = None
        self.reload = True

    def off(self):
        if not self.is_on():
            return

        self.__intensity_prev = self.intensity
        self.intensity = 0.0
        self.reload = True

    def should_reload(self):
        return self.reload

    def toogle(self):
        if self.__intensity_prev is None:
            self.off()
        else:
            self.on()


class DirectionalLight(Light):
    def __init__(self, direction: Vec3d, color: RGBA, intensity: float = 1.0) -> None:
        super().__init__(intensity, color)

        self.direction = -direction

    def set_direction(self, direction):
        self.direction = -direction
        self.reload = True

    def load(self):
        glUseProgram(self.program.id)

        lightDir = glGetUniformLocation(self.program.id, "dirLight1Dir")
        glUniform3f(lightDir, *self.direction.to_list()[:3])

        lightColor = glGetUniformLocation(self.program.id, "dirLight1Color")
        glUniform4f(lightColor, *self.color.to_list())

        lightIntensity = glGetUniformLocation(self.program.id, "dirLight1Intensity")
        glUniform1f(lightIntensity, self.intensity)

        glUseProgram(0)
        self.reload = False


class PointLight(Light):
    def __init__(self, position: Vec3d, color: RGBA, intensity: float = 1.0) -> None:
        super().__init__(intensity, color)

        self.position = position

    def set_color(self, color):
        self.color = color
        self.reload = True

    def set_position(self, position):
        self.position = position
        self.reload = True

    def load(self):
        glUseProgram(self.program.id)

        lightPos = glGetUniformLocation(self.program.id, "pointLight1Pos")
        glUniform3f(lightPos, *self.position.to_list()[:3])

        lightColor = glGetUniformLocation(self.program.id, "pointLight1Color")
        glUniform4f(lightColor, *self.color.to_list())

        lightIntensity = glGetUniformLocation(self.program.id, "pointLight1Intensity")
        glUniform1f(lightIntensity, self.intensity)

        glUseProgram(0)
        self.reload = False


class SpotLight(Light):
    def __init__(self, direction: Vec3d, position: Vec3d, color: RGBA, angle: float, intensity: float = 1.0) -> None:
        super().__init__(intensity, color)

        self.position = position
        self.direction = direction
        self.angle = cos(angle)

    def set_direction(self, direction):
        self.direction = direction
        self.reload = True

    def set_position(self, position: Vec3d):
        self.position = position
        self.reload = True

    def load(self):
        glUseProgram(self.program.id)

        lightPos = glGetUniformLocation(self.program.id, "spotLight1Pos")
        glUniform3f(lightPos, *self.position.to_list()[:3])

        lightColor = glGetUniformLocation(self.program.id, "spotLight1Color")
        glUniform4f(lightColor, *self.color.to_list())

        lightIntensity = glGetUniformLocation(self.program.id, "spotLight1Intensity")
        glUniform1f(lightIntensity, self.intensity)

        lightAngle = glGetUniformLocation(self.program.id, "spotLight1Angle")
        glUniform1f(lightAngle, self.angle)

        lightDir = glGetUniformLocation(self.program.id, "spotLight1Dir")
        glUniform3f(lightDir, *self.direction.to_list()[:3])

        glUseProgram(0)
        self.reload = False
