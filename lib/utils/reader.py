# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import List
from ..math import Vec3d
from ..shape import WingedEdgeShape


def parse_obj(file):
    obj = WingedEdgeShape()

    vertices: List[Vec3d] = []

    with open(file) as f:
        for line in f.readlines():
            line = line.strip()

            if len(line) == 0:
                continue

            cmd = line[0]
            if cmd == "#":
                continue
            elif cmd == "g":
                continue
            elif cmd == "o":
                obj.name = line.split(" ")[1]
            elif cmd == "v":
                x, y, z = tuple(map(float, line.split(" ")[1:4]))
                v = Vec3d.point(x, y, z)
                vertices.append(v)
            elif cmd == "f":
                face_vertices = tuple(map(
                    lambda index: vertices[int(index)-1],
                    line.split(" ")[1:]
                ))

                obj.add_face(face_vertices, ())
            else:
                print("invalid line:", line)

    return obj
