# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

import numpy as np
from typing import List
from PIL import Image
from ..math import Vec3d
from ..shape import WingedEdgeShape, color


def parse_obj(file):
    obj = WingedEdgeShape()

    vertices: List[Vec3d] = []
    texture_vertices: List[Vec3d] = []
    normal_vertices: List[Vec3d] = []

    face_color = color.RGBA.gray()
    border_color = color.RGBA.red()
    random_face_color = False
    random_face_colors = []

    transform_fns_stack = []

    with open(file) as f:
        for line in f.readlines():
            line = line.strip()

            if len(line) == 0:
                continue

            tokenized = line.strip().split(" ")

            cmd = "#" if line[0] == "#" else tokenized[0]
            if cmd == "#":
                words = tokenized[1:]
                # unofficial color support
                if words[0] == "ceng487":
                    if words[1] == "face_color":
                        r, g, b = tuple(map(float, words[2:]))
                        face_color = color.RGBA(r, g, b, 1.0)
                    elif words[1] == "random_face_color":
                        random_face_color = words[2] == "on"
                        if random_face_color:
                            for _ in range(25):
                                gray_scale_color = np.random.uniform(low=0.5, high=0.7)
                                random_face_colors.append(color.RGBA(
                                    gray_scale_color, gray_scale_color, gray_scale_color, 1))
                    elif words[1] == "post_transform":
                        if words[2] == "translate":
                            x, y, z = tuple(map(float, words[3:]))
                            transform_fns_stack.append(lambda: obj.translate(x, y, z))
                        elif words[2] == "rotate":
                            x, y, z = tuple(map(float, words[3:]))
                            transform_fns_stack.append(lambda: obj.rotate(x, y, z))
                        elif words[2] == "scale":
                            x, y, z = tuple(map(float, words[3:]))
                            transform_fns_stack.append(lambda: obj.scale(x, y, z))
            elif cmd == "mtllib":
                continue
            elif cmd == "usemtl":
                continue
            elif cmd == "s":
                continue
            elif cmd == "g":
                continue
            elif cmd == "o":
                obj.name = tokenized[1]
            elif cmd == "v":
                x, y, z = tuple(map(float, tokenized[1:4]))
                vertices.append(Vec3d.point(x, y, z))
            elif cmd == "vt":
                u, v = tuple(map(float, tokenized[1:3]))
                texture_vertices.append(Vec3d.point(u, v, 0))
            elif cmd == "vn":
                x, y, z = tuple(map(float, tokenized[1:4]))
                normal_vertices.append(Vec3d.point(x, y, z))
            elif cmd == "f":
                face_vertices = []
                face_normal_vertices = []
                face_texture_vertices = []

                for vertice_indexes in tokenized[1:]:
                    vi, vti, vni = (*map(
                        lambda v: None if v == "" else int(v)-1,
                        vertice_indexes.split("/")
                    ), None, None)[:3]

                    face_vertices.append(vertices[vi])

                    if vti is not None:
                        face_texture_vertices.append(texture_vertices[vti])

                    if vni is not None:
                        face_normal_vertices.append(normal_vertices[vni])

                current_face_color = face_color
                if random_face_color:
                    current_face_color = random_face_colors[np.random.randint(0, high=25)]

                obj.add_face(face_vertices,
                             current_face_color,
                             border_color,
                             texture_vertices=face_texture_vertices)
            else:
                print("invalid line:", line)

    for fn in transform_fns_stack:
        fn()

    return obj


def read_image(file):
    return Image.open(file).transpose(Image.FLIP_TOP_BOTTOM)
