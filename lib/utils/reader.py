# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

import numpy as np
from typing import List
from os.path import join, dirname
from ..math import Vec3d
from ..shape import WingedEdgeShape, color, Texture


def parse_obj(file) -> List[WingedEdgeShape]:
    group = "__ceng487_default_group__"

    vertices: List[Vec3d] = []
    texture_vertices: List[Vec3d] = []
    normal_vertices: List[Vec3d] = []

    face_color = color.RGBA.white()
    border_color = color.RGBA.red()

    random_face_color = False
    random_face_colors = []

    transform_fns_stack = []
    def create_scaler(sx, sy, sz): return lambda o: o.scale(sx, sy, sz)
    def create_rotator(rx, ry, rz): return lambda o: o.rotate(rx, ry, rz)
    def create_translator(tx, ty, tz): return lambda o: o.translate(tx, ty, tz)

    objs = {group: WingedEdgeShape()}

    textures: List[Texture] = []

    with open(file) as f:
        for line in f.readlines():
            obj = objs[group]
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
                            transform_fns_stack.append(create_translator(x, y, z))
                        elif words[2] == "rotate":
                            x, y, z = tuple(map(float, words[3:]))
                            transform_fns_stack.append(create_rotator(x, y, z))
                        elif words[2] == "scale":
                            x, y, z = tuple(map(float, words[3:]))
                            transform_fns_stack.append(create_scaler(x, y, z))
                    elif words[1] == "texture":
                        if len(textures) > 2:
                            print("warning: maximum 2 textures are supported!")
                        else:
                            textures.append(Texture(join(dirname(file), words[2].strip())))
            elif cmd == "mtllib":
                continue
            elif cmd == "usemtl":
                continue
            elif cmd == "s":
                continue
            elif cmd == "g":
                group = "".join(tokenized[1:])
                if group not in objs:
                    obj = WingedEdgeShape()
                    objs[group] = obj
                    obj.name = tokenized[-1]
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
                face_normal_vectors = []
                face_texture_vertices = []

                for vertice_indexes in tokenized[1:]:
                    vi, vti, vni = (*map(
                        lambda v: None if v == "" else int(v)-1,
                        vertice_indexes.split("/")
                    ), None, None)[:3]

                    face_vertices.append(vertices[vi].clone())

                    if vti is not None:
                        face_texture_vertices.append(texture_vertices[vti].clone())

                    if vni is not None:
                        face_normal_vectors.append(normal_vertices[vni].clone())

                current_face_color = face_color
                if random_face_color:
                    current_face_color = random_face_colors[np.random.randint(0, high=25)]

                obj.add_face(face_vertices,
                             current_face_color,
                             border_color,
                             texture_vertices=face_texture_vertices,
                             normal_vectors=face_normal_vectors)
            else:
                print("invalid line:", line)

    result = list(objs.values())

    for obj in result:
        for fn in transform_fns_stack:
            fn(obj)
        for texture in textures:
            obj.use_texture(texture)

    return result
