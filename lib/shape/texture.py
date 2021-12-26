# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021
import numpy as np
from .shader import Program, Resource
from PIL import Image

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Texture(Resource):
    def __init__(self, file: str) -> None:
        super().__init__()
        self.__image = Image.open(file)
        self.id = None

    def use_program(self, program: Program):
        result = super().use_program(program)
        self.__load_to_gpu()
        return result

    def load(self, location="tex1"):
        glUseProgram(self.program.id)

        tex1Location = glGetUniformLocation(self.program.id, location)
        glUniform1i(tex1Location, self.id)

        glActiveTexture(GL_TEXTURE0 + self.id)
        glBindTexture(GL_TEXTURE_2D, self.id)

        glUseProgram(0)

    def __load_to_gpu(self):
        self.id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D,
                     0,
                     GL_RGB,
                     self.__image.size[0],
                     self.__image.size[1],
                     0,
                     GL_RGB,
                     GL_UNSIGNED_BYTE,
                     np.frombuffer(self.__image.tobytes(), dtype=np.uint8))
        glGenerateMipmap(GL_TEXTURE_2D)
