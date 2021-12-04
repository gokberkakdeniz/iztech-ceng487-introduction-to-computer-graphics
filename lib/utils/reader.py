# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import List
from ..math import Vec3d
from ..shape import Shape, color, WingedEdgeShape


def parse_obj(file):
    vertices: List[Vec3d] = []
    obj = WingedEdgeShape()

    with open(file) as f:
        for line in f.readlines():
            line = line.strip()

            if len(line) == 0:
                continue

            cmd = line[0]
            if cmd == "#":
                continue
            elif cmd == "o":
                obj.name = line.split(" ")[1]
            elif cmd == "v":
                x, y, z = list(map(float, line.split(" ")[1:]))
                vertices.append(Vec3d.point(x, y, z))
            elif cmd == "f":
                face_vertices = list(map(
                    lambda index: vertices[int(index)-1],
                    line.split(" ")[1:]
                ))

                obj.add_quad(face_vertices[0],
                             face_vertices[3],
                             face_vertices[2],
                             face_vertices[1])
            else:
                print("invalid line:", line)
    print(obj)
    return obj
