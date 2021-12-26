# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from ..math import Vec3d
from .color import RGBA
from .shader import Resource


class Light(Resource):
    pass


class DirectionalLight(Light):
    def __init__(self, direction: Vec3d, color: RGBA, intensity: float = 1.0) -> None:
        self.__direction = direction
        self.__color = color
        self.__intensity = intensity


class PointLight(Light):
    def __init__(self, position: Vec3d, color: RGBA, intensity: float = 1.0) -> None:
        self.__position = position
        self.__color = color
        self.__intensity = intensity
