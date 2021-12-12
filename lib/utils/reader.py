# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import List

from ..math import Vec3d
from ..shape import WingedEdgeShape, color


def parse_obj(file):
    obj = WingedEdgeShape()

    vertices: List[Vec3d] = []

    face_color = color.RGBA.gray()
    border_color = color.RGBA.red()

    with open(file) as f:
        for line in f.readlines():
            line = line.strip()

            if len(line) == 0:
                continue

            cmd = line[0]
            if cmd == "#":
                words = line[1:].strip().split(" ")
                # unofficial color support
                if words[0] == "ceng487":
                    if words[1] == "face_color":
                        r, g, b = tuple(map(float, words[2:]))
                        face_color = color.RGBA(r, g, b, 1.0)
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

                obj.add_face(face_vertices, face_color, border_color)
            else:
                print("invalid line:", line)

    return obj
