# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from math import cos, pi, sin
from .object3d import Object3d
from .shape import Shape
from . import color
from ..math import Vec3d


class Sphere(Object3d):
    def __init__(self):
        self.circle_count = 4
        self.circle_point_count = 6

        super().__init__(
            subdivisions=self._calculate_subdivisions()
        )

    def _calculate_unit_points(self):
        unit_points = []

        for i in range(self.circle_point_count):
            theta = 2.0 * pi * i / self.circle_point_count

            x = cos(theta)
            z = sin(theta)

            unit_points.append((x, z))

        return unit_points

    def _calculate_subdivisions(self):
        unit_points = self._calculate_unit_points()

        shapes = []
        previous_points = None
        stack = None
        matrix = None
        if hasattr(self, "subdivisions") and len(self.subdivisions) > 0:
            stack = self.subdivisions[0].stack
            matrix = self.subdivisions[0].matrix

        for y in range(-self.circle_count, self.circle_count + 1):
            y_fixed = y / self.circle_count
            scale_factor = (1 - abs(y_fixed) ** 2) ** 0.5

            current_points = []
            for x, z in unit_points:
                current_points.append(
                    Vec3d.point(
                        x * scale_factor, y_fixed, z * scale_factor
                    )
                )

            if previous_points is not None:
                for i in range(self.circle_point_count):
                    shapes.append(
                        Shape.quadrilateral(
                            previous_points[i],
                            previous_points[(i+1) % self.circle_point_count],
                            current_points[(i+1) % self.circle_point_count],
                            current_points[i],
                            color=color.GRAY,
                            state=(stack, matrix)
                        )
                    )
            previous_points = current_points
        return shapes

    def increase_subdivisions(self):
        self.circle_count += 1
        self.circle_point_count += 1

        self.subdivisions = self._calculate_subdivisions()

    def decrease_subdivisions(self):
        if self.circle_count < 4 or self.circle_point_count < 6:
            return

        self.circle_count -= 1
        self.circle_point_count -= 1

        self.subdivisions = self._calculate_subdivisions()
