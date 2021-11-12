# CENG 487 Assignment2 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from typing import List
from .shape import Shape


class Object3d:
    def __init__(self, subdivisions: List[Shape]) -> None:
        self.subdivisions = subdivisions

    def increase_subdivisions(self):
        pass

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

    def __str__(self) -> str:
        return self.__class__.__name__ + "(subdivisions=[" + ", ".join(map(str, self.subdivisions)) + "])"
