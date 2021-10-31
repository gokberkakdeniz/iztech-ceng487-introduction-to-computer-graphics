
# CENG 487 Assignment1 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from abc import ABC, abstractmethod
from typing import List
from .shape import Shape
from ..matrix import Mat3d


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

    def rotate(self, theta_0, theta_1, theta_2, order="xyz"):
        for division in self.subdivisions:
            division.rotate(theta_0, theta_1, theta_2, order)

    def scale(self, factor):
        for division in self.subdivisions:
            division.scale(factor, factor, factor)

    def undo(self):
        for division in self.subdivisions:
            division.undo()
