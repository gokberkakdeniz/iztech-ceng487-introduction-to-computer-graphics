# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from math import cos, pi, sin
from .object3d import Object3d
from .shape import Shape
from . import color
from ..vector import Vec3d


class Torus(Object3d):
    def __init__(self):
        self.circle_count = 7
        self.circle_point_count = 6

        super().__init__(
            subdivisions=self._calculate_subdivisions()
        )

    def _calculate_subdivisions(self):
        shapes = []
        previous_points = None
        stack = []
        if hasattr(self, "subdivisions") and len(self.subdivisions) > 0:
            stack = self.subdivisions[0].stack

        for i in range(self.circle_count+1):
            theta = 2.0 * pi * i / self.circle_count

            center_x = 0.75 * cos(theta)
            center_z = 0.75 * sin(theta)

            current_points = []
            for i in range(self.circle_point_count):
                theta_2 = 2.0 * pi * i / self.circle_point_count

                x = center_x + 0.25 * cos(theta_2)
                y = 0.25 * sin(theta_2)
                z = center_z

                current_points.append(Vec3d.point(x, y, z))

            if previous_points is not None:
                for i in range(self.circle_point_count+1):
                    shapes.append(
                        Shape.quadrilateral(
                            previous_points[i % self.circle_point_count],
                            previous_points[(i+1) % self.circle_point_count],
                            current_points[(i+1) % self.circle_point_count],
                            current_points[i % self.circle_point_count],
                            color=color.GRAY,
                            stack=stack
                        )
                    )
            previous_points = current_points
        return shapes

    def increase_subdivisions(self):
        self.circle_count += 1
        self.circle_point_count += 1

        self.subdivisions = self._calculate_subdivisions()

    def decrease_subdivisions(self):
        if self.circle_count < 7 or self.circle_point_count < 6:
            return

        self.circle_count -= 1
        self.circle_point_count -= 1

        self.subdivisions = self._calculate_subdivisions()
