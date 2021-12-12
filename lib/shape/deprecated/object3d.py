# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

import operator
from functools import reduce
from typing import List
from .shape import color, Shape
from .. import Drawable


class Object3d(Drawable):
    def __init__(self, subdivisions: List[Shape]) -> None:
        self.subdivisions = subdivisions
        self.level = 0

    def increase_subdivisions(self):
        new_subdivisions = []
        for subdivision in self.subdivisions:
            center = reduce(operator.add, subdivision.vertices) / \
                len(subdivision.vertices)
            vertices = []
            for i in range(4):
                vertices.append(subdivision.vertices[i])
                vertices.append(
                    (subdivision.vertices[i] +
                     subdivision.vertices[(i+1) % 4]) / 2
                )
            for i in range(0, 8, 2):
                new_subdivisions.append(
                    Shape.quadrilateral(
                        vertices[i],
                        vertices[i+1],
                        center,
                        vertices[(i-1) % 8],
                        color=color.GRAY
                    )
                )
        self.subdivisions = new_subdivisions
        self.level += 1

    def decrease_subdivisions(self):
        if self.level == 0:
            return

        new_subdivisions = []
        for i in range(0, len(self.subdivisions), 4):
            new_subdivisions.append(
                Shape.quadrilateral(
                    self.subdivisions[i].vertices[0],
                    self.subdivisions[i+1].vertices[0],
                    self.subdivisions[i+2].vertices[0],
                    self.subdivisions[i+3].vertices[0],
                    color=color.GRAY
                )
            )

        self.subdivisions = new_subdivisions
        self.level -= 1

    def draw(self, border=True, background=True):
        for division in self.subdivisions:
            division.draw(border, background)

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
