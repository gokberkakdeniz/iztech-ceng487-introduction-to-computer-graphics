
from abc import ABC, abstractmethod
from typing import List

from lib.matrix import Mat3d
from .shape import Shape


class Object3d(ABC):
    def __init__(self, subdivisions: List[Shape]) -> None:
        super().__init__()
        self.subdivisions = subdivisions

    @abstractmethod
    def increase_subdivisions(self):
        pass

    @abstractmethod
    def decrease_subdivisions(self):
        pass

    def draw(self):
        for division in self.subdivisions:
            division.draw()

    def draw_border(self):
        for division in self.subdivisions:
            division.draw_border()

    def rotate(self, theta_x, theta_y, theta_z):
        Tx = Mat3d.rotation_x_matrix(theta_x)
        Ty = Mat3d.rotation_y_matrix(theta_y)
        Tz = Mat3d.rotation_z_matrix(theta_z)
        for division in self.subdivisions:
            division.transform(Tx)
            division.transform(Ty)
            division.transform(Tz)

    def scale(self, factor):
        S = Mat3d.scaling_matrix(factor, factor, factor)
        for division in self.subdivisions:
            division.transform(S)
