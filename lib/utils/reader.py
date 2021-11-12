# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from lib.shape.object3d import Object3d
from lib.vector import Vec3d
from lib.shape import Shape, color


def parse_obj(file):
    vertices = []
    faces = []
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()

            if len(line) == 0:
                continue

            cmd = line[0]
            if cmd == "#":
                continue
            elif cmd == "o":
                pass
            elif cmd == "v":
                x, y, z = list(map(float, line.split(" ")[1:]))
                vertices.append(Vec3d.point(x, y, z))
            elif cmd == "f":
                face_vertices = list(map(
                    lambda index: vertices[int(index)-1],
                    line.split(" ")[1:]
                ))
                face = Shape(vertices=face_vertices, color=color.GRAY)
                faces.append(face)
            else:
                print("invalid line:", line)
    return Object3d(subdivisions=faces)
