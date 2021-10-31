# CENG 487 Assignment1 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from math import cos, pi, sin
from . import color
from ..vector import Vec3d
from .object3d import Object3d
from .shape import Shape


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

        top = Shape(top_vertices, color=color.GRAY)
        bottom = Shape(bottom_vertices, color=color.GRAY)

        shapes = [top, bottom]

        for i in range(point_count):
            shapes.append(
                Shape.quadrilateral(
                    top_vertices[i],
                    top_vertices[(i+1) % point_count],
                    bottom_vertices[(i+1) % point_count],
                    bottom_vertices[i],
                    color=color.GRAY
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
