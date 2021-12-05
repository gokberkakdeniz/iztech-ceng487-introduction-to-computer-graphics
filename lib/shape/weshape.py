# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import List, Tuple
from copy import deepcopy
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from lib.utils.bidict import bidict

from . import Drawable, color
from ..math import Vec3d, Mat3d
from .edge import WingedEdge


class WingedEdgeShape(Drawable):
    __object_index = 1

    def __init__(self,
                 name: str = None,
                 state=(None, None)):
        self.name = name or f'shape_{self.__object_index}'

        # Dictionary: hash(vec3d) -> vec3d
        # the hashes cannot be used as index because when the vertices
        # are transformed hash value is changed. so this dictionary is
        # used to keep vertices single instance only.
        self._vertices_cache: dict[int, Vec3d] = {}
        # Bidirectional Dictionary: primary_key <-> hash(vec3d)
        # The vertice indexes are stored here. To perform transformations
        # in O(1), it is bidirectional.
        self._vertices: bidict[int, int] = bidict()  # bidirectional hash table
        self._vertice_index = -1

        self._adj_edges: List[WingedEdge] = []
        self._adj_faces: List[int] = []
        self._adj_vertices: dict[int, int] = {}

        self._quad_complements: bidict[int, int] = bidict()
        self._colors = []

        self._stack = (state[0] or []).copy()
        self._matrix = state[1] or Mat3d.identity()

        if state[0] is not None:
            for v_id in self._vertices_cache:
                self.__transform_vertices(v_id, self._matrix)

        self.__printed = True
        self.__object_index += 1

    @staticmethod
    def quadrilateral(
        vertice0=Vec3d,
        vertice1=Vec3d,
        vertice2=Vec3d,
        vertice3=Vec3d,
        color0: Tuple[int, int, int] = color.WHITE,
        color1: Tuple[int, int, int] = color.WHITE,
        color2: Tuple[int, int, int] = color.WHITE,
        color3: Tuple[int, int, int] = color.WHITE
    ):
        obj = WingedEdgeShape()

        obj.add_quad_face(vertice0, vertice1, vertice2, vertice3,
                          color0,   color1,   color2,   color3)

        return obj

    @ staticmethod
    def triangle(
        vertice0=Vec3d,
        vertice1=Vec3d,
        vertice2=Vec3d,
        color0: Tuple[int, int, int] = color.WHITE,
        color1: Tuple[int, int, int] = color.WHITE,
        color2: Tuple[int, int, int] = color.WHITE,
    ):
        obj = WingedEdgeShape()

        obj.add_tri_face(vertice0, vertice1, vertice2,
                         color0,   color1,   color2)

        return obj

    def draw(self, border=True) -> None:
        if not self.__printed:
            self.__repr__()

        for f_id, e_id in enumerate(self._adj_faces):
            e = self._adj_edges[e_id]
            e_next: WingedEdge = self._adj_edges[e.edge_left_forward]

            h_v1 = self._vertices.get_right(e.vert_origin)
            h_v2 = self._vertices.get_right(e.vert_dest)
            h_v3 = self._vertices.get_right(e_next.vert_dest)

            v1 = self._vertices_cache[h_v1]
            v2 = self._vertices_cache[h_v2]
            v3 = self._vertices_cache[h_v3]
            v4 = None

            if self._quad_complements.has_left(f_id):
                f_c_id = self._quad_complements.get_right(f_id)
                e_c_id = self._adj_faces[f_c_id]
                e_c = self._adj_edges[e_c_id]
                e_c_next: WingedEdge = self._adj_edges[e_c.edge_left_forward]
                h_v4 = self._vertices.get_right(e_c_next.vert_origin)
                v4 = self._vertices_cache[h_v4]

                # preserve ccw order
                v2, v4 = v4, v2
                v3, v4 = v4, v3
            elif self._quad_complements.has_right(f_id):
                continue

            if not self.__printed:
                print(e_id, "=>", e)
                print(" ", "=>", v1, v2, v3, v4)

            if border:
                glLineWidth(2)
                glColor3f(*color.RED)
                glBegin(GL_LINE_STRIP)
                glVertex4f(*v1)
                glVertex4f(*v2)
                glVertex4f(*v3)
                if v4 is not None:
                    glVertex4f(*v4)
                glVertex4f(*v1)
                glEnd()

            glColor3f(*color.GRAY)
            # TODO: check performance
            glBegin(GL_TRIANGLES if v4 is None else GL_POLYGON)
            glVertex4f(*v1)
            glVertex4f(*v2)
            glVertex4f(*v3)
            if v4 is not None:
                glVertex4f(*v4)
            glEnd()

        self.__printed = True

    def rotate(self, theta_0: float, theta_1: float, theta_2: float, order="xyz") -> None:
        R = Mat3d.rotation_matrix(theta_0, theta_1, theta_2, order)
        self._matrix = R @ self._matrix

        self.__transform_vertices(R)

        self._stack.append(('R', order, theta_0, theta_1, theta_2))

    def translate(self, tx: float, ty: float, tz: float) -> None:
        T = Mat3d.translation_matrix(tx, ty, tz)
        self._matrix = T @ self._matrix

        self.__transform_vertices(T)

        self._stack.append(('T', tx, ty, tz))

    def scale(self, sx: float, sy: float, sz: float) -> None:
        S = Mat3d.scaling_matrix(sx, sy, sz)
        self._matrix = S @ self._matrix

        self.__transform_vertices(S)

        self._stack.append(('S', sx, sy, sz))

    def undo(self) -> None:
        if len(self._stack) == 0:
            return

        transformation = self._stack.pop()

        if transformation[0] == 'S':
            sx = 1 / transformation[1]
            sy = 1 / transformation[2]
            sz = 1 / transformation[3]
            self.scale(sx, sy, sz)
        elif transformation[0] == 'T':
            tx = -transformation[1]
            ty = -transformation[2]
            tz = -transformation[3]
            self.translate(tx, ty, tz)
        elif transformation[0] == 'R':
            order = transformation[1][::-1]
            theta_1 = -transformation[4]
            theta_2 = -transformation[3]
            theta_3 = -transformation[2]
            self.rotate(theta_1, theta_2, theta_3, order)
        else:
            self._stack.append(transformation)
            return

        self._stack.pop()

    def clone(self) -> 'WingedEdgeShape':
        # TODO: delete this
        # obj = WingedEdgeShape()

        # obj.name = self.name
        # obj._vertices = deepcopy(self._vertices)
        # obj._adj_edges = deepcopy(self._adj_edges)
        # obj._adj_faces = deepcopy(self._adj_faces)
        # obj._adj_vertices = deepcopy(self._adj_vertices)
        # obj._stack = deepcopy(self._stack)
        # obj._colors = deepcopy(self._colors)
        # obj._matrix = deepcopy(self._matrix)

        return deepcopy(self)

    def add_tri_face(
            self,
            vertice0=Vec3d,
            vertice1=Vec3d,
            vertice2=Vec3d,
            color0: Tuple[int, int, int] = color.WHITE,
            color1: Tuple[int, int, int] = color.WHITE,
            color2: Tuple[int, int, int] = color.WHITE
    ):
        # TODO: implement color support
        i_v0 = self.__register_vertice(vertice0)
        i_v1 = self.__register_vertice(vertice1)
        i_v2 = self.__register_vertice(vertice2)

        f_index = len(self._adj_faces)

        e0_index = self._adj_vertices.get(i_v0)
        e0 = self._adj_edges[e0_index] if e0_index is not None else None

        e1_index = len(self._adj_edges)
        e2_index = e1_index + 1

        e1 = WingedEdge()
        e1.set_vert(i_v1, i_v2)
        e1.set_face(f_index, None)
        e1.set_edge(e0_index,
                    e2_index,
                    self._adj_vertices.get(i_v1),
                    None)
        self._adj_edges.append(e1)

        e2 = WingedEdge()
        e2.set_vert(i_v2, i_v0)
        e2.set_face(f_index, None)
        e2.set_edge(e1_index,
                    e0_index,
                    None,
                    self._adj_vertices.get(i_v0))
        self._adj_edges.append(e2)

        self._adj_faces.append(e1_index)

        self._adj_vertices[i_v2] = e1_index

        if e0 is not None:
            e0.set_edge_right(e1_index, e2_index)

    def add_quad_face(
        self,
        vertice0=Vec3d,
        vertice1=Vec3d,
        vertice2=Vec3d,
        vertice3=Vec3d,
        color0: Tuple[int, int, int] = color.WHITE,
        color1: Tuple[int, int, int] = color.WHITE,
        color2: Tuple[int, int, int] = color.WHITE,
        color3: Tuple[int, int, int] = color.WHITE
    ):
        face1_index = len(self._adj_faces)
        face2_index = face1_index + 1

        self.add_tri_face(vertice0, vertice1, vertice3,
                          color0, color1, color3)
        self.add_tri_face(vertice3, vertice1, vertice2,
                          color3, color1, color2)

        self._quad_complements.add(face1_index, face2_index)

    def __register_vertice(self, vertice: Vec3d) -> int:
        h_vertice = hash(vertice)

        if h_vertice in self._vertices_cache:
            return self._vertices.get_left(h_vertice)

        self._vertice_index += 1

        self._vertices_cache[h_vertice] = vertice

        self._vertices.add(self._vertice_index, h_vertice)

        return self._vertice_index

    def __transform_vertices(self, matrix: Mat3d):
        for v_id in list(self._vertices_cache.keys()):
            self.__transform_vertice(v_id, matrix)

    def __transform_vertice(self, v_id: int, matrix: Mat3d) -> None:
        old = self._vertices_cache[v_id]
        del self._vertices_cache[v_id]

        new = matrix @ old
        new_id = hash(new)

        self._vertices_cache[new_id] = new
        self._vertices.update_right(
            self._vertices.get_left(v_id),
            new_id
        )

    def __str__(self) -> str:
        len_face = len(self._adj_faces)
        len_edge = len(self._adj_edges)
        len_vert = len(self._adj_vertices)

        return f'Shape(name={self.name}, faces={len_face}, edges={len_edge}, points={len_vert})'

    def __repr__(self) -> str:
        print("____________________________________________________\n")
        print("name:", self.name)
        print("____________________________________________________\n")

        print("v_id".ljust(25), "v")
        for v_id, v in self._vertices_cache.items():
            print(str(v_id).ljust(25), v)

        print("____________________________________________________\n")

        print("f_id".ljust(5), "e_id")
        for f_id, e_id in enumerate(self._adj_faces):
            print(str(f_id).ljust(5), e_id)

        print("____________________________________________________\n")

        # print("e_id".ljust(5), "e")
        # for e_id, e in enumerate(self._adj_edges):
        #     v = f'{self._vertices.get(e.vert_origin)}, {self._vertices.get(e.vert_dest)}'
        #     f = f'{e.face_left}, {e.face_right}'
        #     e = f'{e.edge_left_back}, {e.edge_left_forward}, {e.edge_right_back}, {e.edge_right_forward}'
        #     print(str(e_id).ljust(5), f'Edge(v=({v}); f=({f}); e=({e}))')

        print("____________________________________________________\n")

        # print("v_id".ljust(35), "e_id")
        # for v_id, e_id in self._adj_vertices.items():
        #     print(str(self._vertices[v_id]).ljust(35), e_id)

        print("____________________________________________________\n")


__all__ = [WingedEdgeShape]
