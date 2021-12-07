# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import List, Tuple, Union
from copy import deepcopy
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from lib.utils.bidict import bidict

from .. import color
from .edge import WingedEdge
from ..shape import Shape
from ...math import Vec3d, Mat3d


def debug(*args, **kwargs):
    if not debug.__dict__["stop"]:
        print(*args, **kwargs)


debug.__dict__["stop"] = False


class WingedEdgeShape(Shape):
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

        self.__object_index += 1

        self.__F = []
        self.__E = []

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

        obj.add_tri_face(vertice0, vertice1, vertice2,
                         color0,   color1,   color2)

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
            if self.__is_face_right_complement_of_quad(f_id):
                continue

            v1, v2, v3 = self.__get_face_vertices(f_id)
            v4 = None

            if self.__is_face_left_complement_of_quad(f_id):
                fc_id = self._quad_complements.get_right(f_id)
                v4, _, _ = self.__get_face_vertices(fc_id)

                # keep in ccw order
                v2, v3 = v3, v2

            debug(f'F{f_id}:', *[self._vertices.get_left(hash(v))
                  for v in [v1, v2, v3, v4]])

            if len(self.__F) > 0:
                glPointSize(4)
                glColor3f(*colors[f_id % len(colors)])
                glBegin(GL_POINTS)
                glVertex(*self.__F[f_id])
                glEnd()

            if border:
                glLineWidth(2)
                # glColor3f(*colors[f_id % len(colors)])
                glColor(*color.BLACK)
                self.__gl_vertex_safe(v1, v2, v3, v4, border=True)

            glColor3f(*colors[f_id % len(colors)])
            self.__gl_vertex_safe(v1, v2, v3, v4, border=False)
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
        # raise Exception("Not implemented exception! (will be fixed...)")
        # TODO: implement color support
        i_v0 = self.__register_vertice(vertice0)
        i_v1 = self.__register_vertice(vertice1)
        i_v2 = self.__register_vertice(vertice2)

        debug(i_v0, i_v1, i_v2)

        f_index = len(self._adj_faces)

        e0_index = self.__get_edge_index_safe(i_v0, i_v1)
        e1_index = self.__get_edge_index_safe(i_v1, i_v2)
        e2_index = self.__get_edge_index_safe(i_v2, i_v0)

        e0 = self._adj_edges[e0_index]
        e1 = self._adj_edges[e1_index]
        e2 = self._adj_edges[e2_index]

        debug(e0)
        debug(e1)
        debug(e2)

        if e0.vert_origin == None:
            e0.set_vert(i_v0, i_v1)
            e0.face_left = f_index
            e0.set_edge_left(e2_index, e1_index)
            self._adj_vertices[i_v0] = e0_index
        else:
            e0.face_right = f_index
            e0.set_edge_right(e1_index, e2_index)

        if e1.vert_origin == None:
            e1.set_vert(i_v1, i_v2)
            e1.face_left = f_index
            e1.set_edge_left(e0_index, e2_index)
            self._adj_vertices[i_v1] = e1_index
        else:
            e1.face_right = f_index
            e1.set_edge_right(e2_index, e0_index)

        if e2.vert_origin == None:
            e2.set_vert(i_v2, i_v0)
            e2.face_left = f_index
            e2.set_edge_left(e1_index, e0_index)
            self._adj_vertices[i_v2] = e2_index
        else:
            e2.face_right = f_index
            e2.set_edge_right(e0_index, e1_index)

        self._adj_faces.append(e2_index)

        debug(e0)
        debug(e1)
        debug(e2)

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

        # vertice_center = (vertice0 + vertice1 + vertice2 + vertice3) / 4

        # self.add_tri_face(vertice0, vertice1, vertice_center,
        #                   color0, color1, color2)
        # self.add_tri_face(vertice_center, vertice2, vertice1,
        #                   color0, color1, color2)

        # self.add_tri_face(vertice3, vertice_center, vertice2,
        #                   color2, color0, color3)
        # self.add_tri_face(vertice_center, vertice0, vertice3,
        #                   color2, color0, color3)

        self.add_tri_face(vertice0, vertice1, vertice2,
                          color0, color1, color2)
        self.add_tri_face(vertice2, vertice0, vertice3,
                          color2, color0, color3)

        print(repr(self))

        self._quad_complements.add(face1_index, face2_index)

    def subdivide_catmull_clark(self):
        # TODO: check if fully quad mesh

        # calculate face points
        self.__F = [None] * len(self._adj_faces)
        for f_id in range(len(self._adj_faces)):
            # debug(self._adj_edges[self._adj_faces[f_id]])
            v1, v2, v3, v4 = self.__get_face_vertices(f_id)
            v_avg = (v1 + v2 + v3 + v4) / 4

            self.__F[f_id] = v_avg

        # calculate edge_points
        self.__E = [None] * len(self._adj_edges)
        for f_id, e_id in enumerate(self._adj_faces):
            if self.__E[e_id] is not None:
                continue

            e1 = self._adj_edges[e_id]
            e2_id = None
            e2 = None

            if self.__is_face_left_complement_of_quad(f_id):
                e2_id = e1.edge_left_back
            else:
                e2_id = e1.edge_left_forward
            # debug(e1)
            # self.__E[e_id] = None
            # self.__E[e2_id] = None

    def __get_edge_index_safe(self, vert_origin_id: int, vert_dest_id) -> int:
        e_id = self._adj_vertices.get(vert_origin_id)

        if e_id is not None:
            e = self._adj_edges[e_id]
            if not self.__is_edge_of(e, vert_origin_id, vert_dest_id):
                e_id = self.__find_edge(e_id, vert_origin_id, vert_dest_id)

        if e_id is None:
            e_id = len(self._adj_edges)
            e = WingedEdge()
            self._adj_edges.append(e)

        return e_id

    def __find_edge(self, e_start_id: int, vert_origin_id: int, vert_dest_id: int) -> int:
        # TODO: fix traversing...
        # e_id = e_start_id
        # e = self._adj_edges[e_id]

        # debug(repr(self))
        # debug(
        #     f'searching v{vert_origin_id} -> v{vert_dest_id} from starting e{e_start_id}'
        # )

        # return self.__find_edge_ccw(e_start_id, vert_origin_id, vert_dest_id) \
        #     or self.__find_edge_cw(e_start_id, vert_origin_id, vert_dest_id)

        for e_id, e in enumerate(self._adj_edges):
            if self.__is_edge_of(e, vert_origin_id, vert_dest_id):
                return e_id

        return None

    def __find_edge_ccw(self, e_start_id: int, vert_origin_id: int, vert_dest_id: int) -> int:
        e_id = e_start_id
        e = self._adj_edges[e_id]

        while e is not None:
            e_id = e.edge_left_forward

            if e_id is None:
                break

            e = self._adj_edges[e_id]
            # debug(
            #     f'searching v{vert_origin_id} -> v{vert_dest_id} starting from v{self._adj_edges[e_start_id].vert_origin} -> v{self._adj_edges[e_start_id].vert_dest} :: {e.vert_origin} -> {e.vert_dest}'
            # )

            if self.__is_edge_of(e, vert_origin_id, vert_dest_id):
                return e_id
            elif e.vert_dest == self._adj_edges[e_start_id].vert_origin:
                return None

    def __find_edge_cw(self, e_start_id: int, vert_origin_id: int, vert_dest_id: int) -> int:
        e_id = e_start_id
        e = self._adj_edges[e_id]

        while e is not None:
            e_id = e.edge_right_forward

            if e_id is None:
                break

            e = self._adj_edges[e_id]
            # debug(
            #     f'searching v{vert_origin_id} -> v{vert_dest_id} starting from v{self._adj_edges[e_start_id].vert_origin} -> v{self._adj_edges[e_start_id].vert_dest} :: {e.vert_origin} -> {e.vert_dest}'
            # )

            if self.__is_edge_of(e, vert_origin_id, vert_dest_id):
                return e_id
            elif e.vert_dest == self._adj_edges[e_start_id].vert_origin:
                return None

    def __is_edge_of(self, e: WingedEdge, vert_origin_id: int, vert_dest_id: int):
        return (e.vert_origin == vert_origin_id and e.vert_dest == vert_dest_id)  \
            or (e.vert_origin == vert_dest_id and e.vert_dest == vert_origin_id)

    def __gl_vertex_safe(self, v1: Vec3d, v2: Vec3d, v3: Vec3d, v4: Union[Vec3d, None], border=False) -> None:
        is_quad = v4 is not None

        if border:
            glBegin(GL_LINE_STRIP)
        elif is_quad:
            glBegin(GL_POLYGON)
        else:
            glBegin(GL_TRIANGLES)

        glVertex4f(*v1)
        glVertex4f(*v2)
        glVertex4f(*v3)

        if v4 is not None:
            glVertex4f(*v4)

        if border:
            glVertex4f(*v1)

        glEnd()

    def __get_face_vertices(self, face_id: int) -> List[Vec3d]:
        edge_id = self._adj_faces[face_id]
        edge = self._adj_edges[edge_id]

        h_v1 = self._vertices.get_right(edge.vert_origin)
        h_v2 = self._vertices.get_right(edge.vert_dest)

        if edge.face_left == face_id:
            edge_next: WingedEdge = self._adj_edges[edge.edge_left_forward]

            debug(
                f"F{face_id}: e{edge_id} -> e{edge.edge_left_forward} [LEFT]"
            )

            if edge_next.vert_dest == edge.vert_dest or edge_next.vert_dest == edge.vert_origin:
                h_v3 = self._vertices.get_right(edge_next.vert_origin)
            else:
                h_v3 = self._vertices.get_right(edge_next.vert_dest)
        else:
            edge_next: WingedEdge = self._adj_edges[edge.edge_right_forward]

            debug(
                f"F{face_id}: e{edge_id} -> e{edge.edge_right_forward} :: dest [RIGHT]"
            )

            if edge_next.vert_dest == edge.vert_dest or edge_next.vert_dest == edge.vert_origin:
                h_v3 = self._vertices.get_right(edge_next.vert_origin)
            else:
                h_v3 = self._vertices.get_right(edge_next.vert_dest)

        v1 = self._vertices_cache[h_v1]
        v2 = self._vertices_cache[h_v2]
        v3 = self._vertices_cache[h_v3]

        return [v1, v2, v3]

    def __is_face_left_complement_of_quad(self, face_id: int) -> bool:
        return self._quad_complements.has_left(face_id)

    def __is_face_right_complement_of_quad(self, face_id: int) -> bool:
        return self._quad_complements.has_right(face_id)

    def __is_face_quad(self, face_id: int) -> bool:
        return self.__is_face_left_complement_of_quad(face_id) or self.__is_face_right_complement_of_quad(face_id)

    def __is_face_tri(self, face_id: int) -> bool:
        return not self.__is_face_quad(face_id)

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
