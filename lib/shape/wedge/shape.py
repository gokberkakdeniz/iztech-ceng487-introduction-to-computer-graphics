# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import Generator, Iterable, List, Tuple, Union
from copy import deepcopy
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from itertools import chain
from lib.utils.bidict import bidict

from .. import color
from .edge import WingedEdge
from ..shape import Shape
from ...math import Vec3d, Mat3d


def debug(*args, **kwargs):
    if not debug.__dict__["stop"]:
        print(*args, **kwargs)


debug.__dict__["stop"] = True


class WingedEdgeShape(Shape):
    __object_index = 1

    def __init__(self,
                 name: str = None,
                 state=(None, None)):
        # object properties
        self.name = name or f'shape_{self.__object_index}'
        self.level = 0

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

        # self._quad_complements: bidict[int, int] = bidict()
        self._colors = []

        # transformation matrix and stack
        self._stack = (state[0] or []).copy()
        self._matrix = state[1] or Mat3d.identity()

        # load given state
        if state[0] is not None:
            for v_id in self._vertices_cache:
                self.__transform_vertices(v_id, self._matrix)

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

        obj.add_face((vertice0, vertice1, vertice2, vertice3),
                     (color0, color1, color2, color3))

        return obj

    @staticmethod
    def triangle(
        vertice0=Vec3d,
        vertice1=Vec3d,
        vertice2=Vec3d,
        color0: Tuple[int, int, int] = color.WHITE,
        color1: Tuple[int, int, int] = color.WHITE,
        color2: Tuple[int, int, int] = color.WHITE,
    ):
        obj = WingedEdgeShape()

        obj.add_face((vertice0, vertice1, vertice2),
                     (color0, color1, color2))

        return obj

    def draw(self, border=True) -> None:
        debug("=========")

        colors = [
            (160/255, 81/255, 149/255),
            color.BLUE,
            (255/255, 166/255, 0/255),
            color.CYAN,
            (249/255, 93/255, 106/255),
            color.RED,
            (47/255, 75/255, 124/255),
            color.GREEN,
            (138/255, 171/255, 227/255),
            color.VIOLET,
            (56/255, 242/255, 161/255),
            color.WHITE,
            (242/255, 10/255, 122/255),
        ]
        for f_id in range(len(self._adj_faces)):
            vertices = tuple(self.__get_face_vertices(f_id))

            debug(f'F{f_id}:', *[self._vertices.get_left(hash(v)) for v in vertices])

            if border:
                glLineWidth(2)
                glColor(*color.RED)
                # glColor3f(*colors[f_id % len(colors)])
                self.__gl_vertex(vertices, border=True)

            # glColor3f(*colors[f_id % len(colors)])
            glColor3f(*color.GRAY)
            self.__gl_vertex(vertices, border=False)

        debug("=========")
        for e in self._adj_edges:
            debug(e)
        debug.__dict__["stop"] = True

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
            order = transformation[1][:: -1]
            theta_1 = -transformation[4]
            theta_2 = -transformation[3]
            theta_3 = -transformation[2]
            self.rotate(theta_1, theta_2, theta_3, order)
        else:
            self._stack.append(transformation)
            return

        self._stack.pop()

    def clone(self) -> 'WingedEdgeShape':
        return deepcopy(self)

    def add_face(self, vertices: List[Vec3d], colors: List[Vec3d]):
        v_indexes = [self._register_vertice(v) for v in vertices]
        f_index = len(self._adj_faces)

        for i in range(len(v_indexes)):
            j = (i + 1) % len(v_indexes)
            k = (i + 2) % len(v_indexes)
            l = (i + 3) % len(v_indexes)

            e0_index = self.__get_edge_index_safe(v_indexes[i], v_indexes[j])
            e1_index = self.__get_edge_index_safe(v_indexes[j], v_indexes[k])
            e2_index = self.__get_edge_index_safe(v_indexes[k], v_indexes[l])

            e0 = self._adj_edges[e0_index]
            e1 = self._adj_edges[e1_index]
            e2 = self._adj_edges[e2_index]

            i_v0 = v_indexes[i]
            i_v1 = v_indexes[j]
            i_v2 = v_indexes[k]

            if e0.face_left is None and e0.face_right is None:
                e0.set_vert(i_v0, i_v1)
                e0.face_left = f_index
                e0.set_edge_left(e2_index, e1_index)
                self._adj_vertices[i_v0] = e0_index
            else:
                e0.face_right = f_index
                e0.set_edge_right(e1_index, e2_index)

        self._adj_faces.append(self.__get_edge_index_safe(v_indexes[0], v_indexes[1]))

    def subdivide_catmull_clark(self):
        # calculate face points
        face_points: List[Vec3d] = [None] * len(self._adj_faces)
        for f_id in range(len(self._adj_faces)):
            # debug(self._adj_edges[self._adj_faces[f_id]])
            v1, v2, v3, v4 = self.__get_face_vertices(f_id)

            f_p = (v1 + v2 + v3 + v4) / 4

            face_points[f_id] = f_p

        # calculate edge points
        edge_points: List[Vec3d] = [None] * len(self._adj_edges)
        for e_id, e in enumerate(self._adj_edges):
            ev_o = self._vertices_cache[self._vertices.get_right(e.vert_origin)]
            ev_f = self._vertices_cache[self._vertices.get_right(e.vert_dest)]
            fp_l = face_points[e.face_left]
            fp_r = face_points[e.face_right]

            ep = (ev_o + ev_f + fp_l + fp_r) / 4

            edge_points[e_id] = ep

        # calculate new positions of the original points
        new_points: List[Vec3d] = [None] * len(self._vertices_cache)
        for i_v, h_v in self._vertices.items():
            p = self._vertices_cache[h_v]
            e_id = self._adj_vertices[i_v]

            r = Vec3d.point(0, 0, 0)
            n = 0
            face_ids = set()
            for edge in chain(self.__get_edges_of_vertice(i_v)):
                r += (self._vertices_cache[self._vertices.get_right(edge.vert_origin)]
                      + self._vertices_cache[self._vertices.get_right(edge.vert_dest)])

                face_ids.add(edge.face_left)
                face_ids.add(edge.face_right)

                n += 1
            r = r / (2*n)
            print(len(face_ids), n)

            f = Vec3d.point(0, 0, 0)
            for f_id in face_ids:
                f += face_points[f_id]
            f = f / n

            new_points[i_v] = (f + 2*r + (n - 3) * p) / n

        # calculate new faces
        new_faces = []
        for f_id in range(len(self._adj_faces)):
            face_new_points = tuple(new_points[v_id] for v_id in self.__get_face_vertice_indexes(f_id))
            face_edge_points = tuple(edge_points[e_id] for e_id in self.__get_face_edge_indexes(f_id))
            face_point = face_points[f_id]

            new_faces.append([face_new_points[0], face_edge_points[0], face_point, face_edge_points[3]])
            new_faces.append([face_edge_points[0], face_new_points[1], face_edge_points[1], face_point])
            new_faces.append([face_point, face_edge_points[1], face_new_points[2], face_edge_points[2]])
            new_faces.append([face_edge_points[3], face_point, face_edge_points[2], face_new_points[3]])

        # reset
        self._vertices_cache: dict[int, Vec3d] = {}
        self._vertices: bidict[int, int] = bidict()
        self._vertice_index = -1
        self._adj_edges: List[WingedEdge] = []
        self._adj_faces: List[int] = []
        self._adj_vertices: dict[int, int] = {}
        self._colors = []

        # add new faces
        for new_face in new_faces:
            self.add_face(new_face, [])

        # for f_id in range(len(self._adj_faces)):
        #     print(f'# face = {f_id}')
        #     i = 0
        #     for v_id in self.__get_face_vertice_indexes(f_id):
        #         print(f'  [{i}] {v_id}')
        #         i += 1
        #         if i == 20:
        #             break

        # print(repr(self))

        # exit()

        self.level += 1

    def __get_edges_of_vertice(self, v_id: int):
        # TODO: find by traversing

        for edge in self._adj_edges:
            if edge.vert_dest == v_id or edge.vert_origin == v_id:
                yield edge

    def __get_edge_index_safe(self, vert_origin_id: int, vert_dest_id) -> int:
        e_id = self.__find_edge(vert_origin_id, vert_dest_id)

        if e_id is None:
            e_id = len(self._adj_edges)
            e = WingedEdge()
            e.vert_origin = vert_origin_id
            e.vert_dest = vert_dest_id
            self._adj_edges.append(e)

        return e_id

    def __find_edge(self, vert_origin_id: int, vert_dest_id: int) -> int:
        # TODO: find by traversing

        for e_id, e in enumerate(self._adj_edges):
            if self.__is_edge_of(e, vert_origin_id, vert_dest_id):
                return e_id

        return None

    def __is_edge_of(self, e: WingedEdge, vert_origin_id: int, vert_dest_id: int):
        return (e.vert_origin == vert_origin_id and e.vert_dest == vert_dest_id)  \
            or (e.vert_origin == vert_dest_id and e.vert_dest == vert_origin_id)

    def __gl_vertex(self, vertices: List[Vec3d], border=False) -> None:
        is_polygon = len(vertices) > 3

        if border:
            glBegin(GL_LINE_STRIP)
        elif is_polygon:
            glBegin(GL_POLYGON)
        else:
            glBegin(GL_TRIANGLES)

        for vertice in vertices:
            glVertex4f(*vertice)

        if border:
            glVertex4f(*vertices[0])

        glEnd()

    def __get_face_vertice_indexes(self, face_id) -> Generator[int, None, None]:
        edge = self._adj_edges[self._adj_faces[face_id]]

        first = None
        while True:
            if edge.face_left == face_id:
                v_id = edge.vert_origin
                edge = self._adj_edges[edge.edge_left_forward]
            else:
                v_id = edge.vert_dest
                edge = self._adj_edges[edge.edge_right_back]

            if first is None:
                first = v_id
            elif first == v_id:
                break

            yield v_id

    def __get_face_vertices(self, face_id: int) -> Generator[Vec3d, None, None]:
        for v_id in self.__get_face_vertice_indexes(face_id):
            yield self._vertices_cache[self._vertices.get_right(v_id)]

    def __get_face_edge_indexes(self, face_id: int) -> Generator[int, None, None]:
        e_id = self._adj_faces[face_id]

        first = e_id
        while True:
            edge = self._adj_edges[e_id]

            yield e_id

            if edge.face_left == face_id:
                e_id = edge.edge_left_forward
            else:
                e_id = edge.edge_right_back

            if first == e_id:
                break

    def __get_face_edges(self, face_id: int) -> Generator[WingedEdge, None, None]:
        for e_id in self.__get_face_edge_indexes(face_id):
            yield self._adj_edges[e_id]

    def __register_vertice(self, vertice: Vec3d) -> int:
        h_vertice = hash(vertice)

        if h_vertice in self._vertices_cache:
            return self._vertices.get_left(h_vertice)

        self._vertice_index += 1

        self._vertices_cache[h_vertice] = vertice

        self._vertices.add(self._vertice_index, h_vertice)

        return self._vertice_index

    def __transform_vertices(self, matrix: Mat3d) -> None:
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
        result = []
        result.append("____________________________________________________\n")
        result.append("name: " + self.name)
        result.append("____________________________________________________\n")

        result.append("v_id".ljust(5) + " v")
        for v_id, v_hash in self._vertices.l2r.items():
            result.append(
                f'{str(v_id).ljust(5)} {self._vertices_cache[v_hash]}'
            )

        result.append("____________________________________________________\n")

        result.append("f_id".ljust(5) + " e_id")
        for f_id, e_id in enumerate(self._adj_faces):
            result.append(
                f'{str(f_id).ljust(5)} {e_id}'
            )

        result.append("____________________________________________________\n")

        result.append("e_id".ljust(5) + " e")
        for e_id, e in enumerate(self._adj_edges):
            v = f'{e.vert_origin}, {e.vert_dest}'
            f = f'{e.face_left}, {e.face_right}'
            e = f'{e.edge_left_back}, {e.edge_left_forward}, {e.edge_right_back}, {e.edge_right_forward}'
            result.append(
                f'{str(e_id).ljust(5)} Edge(v=({v}); f=({f}); e=({e}))'
            )

        result.append("____________________________________________________\n")

        result.append("v_id".ljust(5) + " e_id")
        for v_id, e_id in self._adj_vertices.items():
            result.append(f'{str(v_id).ljust(5)} {e_id}')

        result.append("____________________________________________________\n")

        return "\n".join(result)

    _register_vertice = __register_vertice


__all__ = [WingedEdgeShape]
