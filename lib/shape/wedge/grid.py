
from typing import Tuple

from lib.math.vector import Vec3d
from .shape import WingedEdgeShape


class Grid(WingedEdgeShape):
    def __init__(self,
                 shape: Tuple[int, int],
                 name: str = None):
        super().__init__(name=name or f'shape_{self.__object_index}')
        size_x, size_z = shape

        vertices = []
        for x in range(-size_x, size_x + 1, 2):
            for z in range(-size_z, size_z + 1, 2):
                vertices.append(Vec3d.point(x, 0, z))

        for x in range(0, size_x * size_z):
            indexX = x % size_x
            indexZ = x // size_z
            id1 = indexZ * (size_x + 1) + indexX
            id2 = (indexZ + 1) * (size_x + 1) + indexX
            self.add_face([vertices[id1], vertices[id1 + 1], vertices[id2 + 1], vertices[id2]])
