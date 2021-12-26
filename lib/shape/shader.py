# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import List, Union
from typing_extensions import Literal
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from abc import ABC, abstractmethod

ShaderType = Literal["vertex", "geometry", "fragment", "compute", "tessellation_control", "tessellation_evaluation"]


class Shader:
    def __init__(self, file: str, type: ShaderType = None) -> None:
        self.type = type or file.split(".")[-1]
        self.status = None
        self.id = glCreateShader(self.__get_opengl_shader_type_constant())

        with open(file, "r") as f:
            glShaderSource(self.id, f.read())

        glCompileShader(self.id)

        glGetShaderiv(self.id, GL_COMPILE_STATUS, self.status)

        if self.status == GL_FALSE:
            strInfoLog = glGetShaderInfoLog(self.id)
            raise Exception("Compile failed: " + strInfoLog)

    def __get_opengl_shader_type_constant(self):
        return {
            "vert": GL_VERTEX_SHADER,
            "vertex": GL_VERTEX_SHADER,

            "geom": GL_GEOMETRY_SHADER,
            "geometry": GL_GEOMETRY_SHADER,

            "frag": GL_FRAGMENT_SHADER,
            "fragment": GL_FRAGMENT_SHADER,

            "comp": GL_COMPUTE_SHADER,
            "compute": GL_COMPUTE_SHADER,

            "tesc": GL_TESS_CONTROL_SHADER,
            "tessellation_control": GL_TESS_CONTROL_SHADER,

            "tese": GL_TESS_EVALUATION_SHADER,
            "tessellation_evaluation": GL_TESS_EVALUATION_SHADER,
        }.get(self.type, None)


class Program:
    def __init__(self, shaders: List[Shader], resources: List['Resource'] = []) -> None:
        self.id = glCreateProgram()

        for shader in shaders:
            glAttachShader(self.id, shader.id)

        glLinkProgram(self.id)

        status = glGetProgramiv(self.id, GL_LINK_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetProgramInfoLog(self.id)
            raise Exception("Linker failure: " + str(strInfoLog))

        for shader in shaders:
            glDetachShader(self.id, shader.id)

        for shader in shaders:
            glDeleteShader(shader.id)

        for res in resources:
            res.use_program(self)


class Resource(ABC):
    def __init__(self) -> None:
        self.program = None

    def use_program(self, program: Program):
        self.program = program

    @abstractmethod
    def load(self):
        pass
