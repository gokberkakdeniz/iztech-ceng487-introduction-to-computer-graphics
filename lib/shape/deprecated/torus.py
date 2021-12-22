# CENG 487 Assignment5 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from math import cos, pi, sin

from .. import color
from .object3d import Object3d
from .shape import DeprecatedShape
from ...math import Vec3d, Mat3d


class DeprecatedTorus(Object3d):
    def __init__(self):
        self.circle_count = 7
        self.circle_point_count = 6

        super().__init__(
            subdivisions=self._calculate_subdivisions()
        )
        self.rotate(pi/2, 0, 0)

    def _calculate_subdivisions(self):
        shapes = []
        previous_points = None
        stack = None
        matrix = None
        if hasattr(self, "subdivisions") and len(self.subdivisions) > 0:
            stack = self.subdivisions[0].stack
            matrix = self.subdivisions[0].matrix

        theta_x = 2.0 * pi / self.circle_count
        theta_y = 2.0 * pi / self.circle_point_count

        for i in range(self.circle_count+1):
            theta_xi = theta_x * i
            Ry = Mat3d.rotation_y_matrix(-theta_xi)

            center_x = 0.75 * cos(theta_xi)
            center_z = 0.75 * sin(theta_xi)

            current_points = []
            for j in range(self.circle_point_count):
                theta_yj = theta_y * j

                p_center = Vec3d.vector(center_x, 0, center_z)
                p_origin = Vec3d.point(
                    0.25 * cos(theta_yj),
                    0.25 * sin(theta_yj),
                    0
                )
                point = p_center + Ry @ p_origin

                current_points.append(point)

            if previous_points is not None:
                for i in range(self.circle_point_count+1):
                    shapes.append(
                        DeprecatedShape.quadrilateral(
                            previous_points[i % self.circle_point_count],
                            previous_points[(i+1) % self.circle_point_count],
                            current_points[(i+1) % self.circle_point_count],
                            current_points[i % self.circle_point_count],
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
        if self.circle_count < 7 or self.circle_point_count < 6:
            return

        self.circle_count -= 1
        self.circle_point_count -= 1

        self.subdivisions = self._calculate_subdivisions()
