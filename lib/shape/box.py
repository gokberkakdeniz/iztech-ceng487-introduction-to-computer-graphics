# CENG 487 Assignment2 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from . import color
from ..vector import Vec3d
from ..matrix import Mat3d
from .shape import Shape
from .object3d import Object3d


class Box(Object3d):
    def __init__(self):
        super().__init__(
            subdivisions=[
                Shape.quadrilateral(  # Top
                    Vec3d.point(1.0, 1.0, -1.0),
                    Vec3d.point(-1.0, 1.0, -1.0),
                    Vec3d.point(-1.0, 1.0, 1.0),
                    Vec3d.point(1.0, 1.0, 1.0),
                    color=color.GRAY
                ),
                Shape.quadrilateral(  # Bottom
                    Vec3d.point(1.0, -1.0, 1.0),
                    Vec3d.point(-1.0, -1.0, 1.0),
                    Vec3d.point(-1.0, -1.0, -1.0),
                    Vec3d.point(1.0, -1.0, -1.0),
                    color=color.GRAY
                ),
                Shape.quadrilateral(  # Front
                    Vec3d.point(1.0, 1.0, 1.0),
                    Vec3d.point(-1.0, 1.0, 1.0),
                    Vec3d.point(-1.0, -1.0, 1.0),
                    Vec3d.point(1.0, -1.0, 1.0),
                    color=color.GRAY
                ),
                Shape.quadrilateral(  # Back
                    Vec3d.point(1.0, -1.0, -1.0),
                    Vec3d.point(-1.0, -1.0, -1.0),
                    Vec3d.point(-1.0, 1.0, -1.0),
                    Vec3d.point(1.0, 1.0, -1.0),
                    color=color.GRAY
                ),
                Shape.quadrilateral(  # Left
                    Vec3d.point(-1.0, 1.0, 1.0),
                    Vec3d.point(-1.0, 1.0, -1.0),
                    Vec3d.point(-1.0, -1.0, -1.0),
                    Vec3d.point(-1.0, -1.0, 1.0),
                    color=color.GRAY
                ),
                Shape.quadrilateral(  # Right
                    Vec3d.point(1.0, 1.0, -1.0),
                    Vec3d.point(1.0, 1.0, 1.0),
                    Vec3d.point(1.0, -1.0, 1.0),
                    Vec3d.point(1.0, -1.0, -1.0),
                    color=color.GRAY
                )
            ]
        )

    def increase_subdivisions(self):
        divided_subdivisions = []

        for subdivision in self.subdivisions:
            halved = subdivision.clone()
            halved.scale(0.5, 0.5, 0.5)

            for vertice in halved:
                new_subdivision = halved.clone()
                new_subdivision.translate(*vertice[:-1])

                divided_subdivisions.append(new_subdivision)

        self.subdivisions = divided_subdivisions

    def decrease_subdivisions(self):
        if len(self.subdivisions) == 6:
            return

        merged_subdivisions = []

        for subdivision in self.subdivisions[::4]:
            doubled = subdivision.clone()
            doubled.scale(2.0, 2.0, 2.0)
            doubled.translate(*(-subdivision[0])[:-1])

            merged_subdivisions.append(doubled)

        self.subdivisions = merged_subdivisions
