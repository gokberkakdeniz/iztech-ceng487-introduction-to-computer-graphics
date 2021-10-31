
from typing import List

import lib.color as Color
from lib.matrix import Mat3d
from lib.object import Object3d
from .vector import Vec3d
from .shape import Shape
import random
from math import cos, pi, sin


class Cylinder(Object3d):
    def __init__(self):
        self.count = 8
        super().__init__(
            subdivisions=Cylinder._calculate_subdivisions(self.count)
        )

    @staticmethod
    def _calculate_subdivisions(point_count):
        top_vertices = []
        bottom_vertices = []

        for i in range(point_count):
            theta = 2.0 * pi * i / point_count

            x = cos(theta)
            z = sin(theta)

            top_vertices.append(Vec3d.point(x, 1, z))
            bottom_vertices.append(Vec3d.point(x, -1, z))

        top = Shape(top_vertices, color=Color.GRAY)
        bottom = Shape(bottom_vertices, color=Color.GRAY)

        shapes = [top, bottom]

        for i in range(point_count):
            shapes.append(
                Shape.quadrilateral(
                    top_vertices[i],
                    top_vertices[(i+1) % point_count],
                    bottom_vertices[(i+1) % point_count],
                    bottom_vertices[i],
                    color=Color.GRAY
                )
            )

        return shapes

    def increase_subdivisions(self):
        self.count *= 2
        self.subdivisions = self._calculate_subdivisions(self.count)

    def decrease_subdivisions(self):
        if self.count < 8:
            return
        self.count //= 2
        self.subdivisions = self._calculate_subdivisions(self.count)
