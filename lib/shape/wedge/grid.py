
from typing import Tuple

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ...math import Vec3d
from .shape import WingedEdgeShape, color


class Grid(WingedEdgeShape):
    def __init__(self,
                 shape: Tuple[int, int],
                 name: str = None):
        super().__init__(name=name)
        self.size_x, self.size_z = shape

        gray = color.RGBA.gray()
        face_color = gray
        border_color = gray

        for xi in range(self.size_x):
            x = xi - self.size_x / 2
            for zi in range(self.size_z):
                z = zi - self.size_z / 2

                self.add_face([Vec3d.point(x, 0, z),
                               Vec3d.point(x+1, 0, z),
                               Vec3d.point(x+1, 0, z+1),
                               Vec3d.point(x, 0, z+1)],
                              face_color,
                              border_color)

    def _get_border_array_for_buffer(self):
        green = color.RGBA.green()
        blue = color.RGBA.blue()

        border_vertices, border_colors = super()._get_border_array_for_buffer(
            lambda v1, v2: (v1.x != 0 or v2.x != 0) and (v1.z != 0 or v2.z != 0)
        )

        border_vertices.extend((
            *Vec3d.point(-self.size_x/2, 0, 0).to_list()[:3],
            *Vec3d.point(self.size_x/2, 0, 0).to_list()[:3],
            *Vec3d.point(0, 0, -self.size_z/2).to_list()[:3],
            *Vec3d.point(0, 0, self.size_z/2).to_list()[:3],
        ))

        border_colors.extend((
            *green.to_list(),
            *green.to_list(),
            *blue.to_list(),
            *blue.to_list(),
        ))

        return (border_vertices, border_colors)

    def draw(self, border=None, background=None) -> None:
        super().draw(border=True, background=False)
