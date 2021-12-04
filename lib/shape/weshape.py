# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import List, Tuple, Union

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from . import Drawable
from ..math import Vec3d, Mat3d

from . import color


class Edge:  # ccw
    def __init__(self) -> None:
        self.vert_origin = None
        self.vert_dest = None

        self.face_left = None
        self.face_right = None

        self.edge_left_back = None
        self.edge_left_forward = None
        self.edge_right_back = None
        self.edge_right_forward = None

    def set_vert(self, origin: Union[int, None], dest: Union[int, None]):
        self.vert_origin = origin
        self.vert_dest = dest

    def set_face(self, left:  Union[int, None], right: Union[int, None]):
        self.face_left = left
        self.face_right = right

    def set_edge(self, left_back: Union[int, None],
                 left_forward: Union[int, None],
                 right_back: Union[int, None],
                 right_forward: Union[int, None]):
        self.edge_left_back = left_back
        self.edge_left_forward = left_forward
        self.edge_right_back = right_back
        self.edge_right_forward = right_forward

    def set_edge_left(self,
                      left_back: Union[int, None],
                      left_forward: Union[int, None]):
        self.edge_left_back = left_back
        self.edge_left_forward = left_forward

    def set_edge_right(self,
                       right_back: Union[int, None],
                       right_forward: Union[int, None]):
        self.edge_right_back = right_back
        self.edge_right_forward = right_forward

    def __str__(self) -> str:
        return f'Edge(\
v=({self.vert_origin}, {self.vert_dest}); \
f=({self.face_left}, {self.face_right}); \
e=({self.edge_left_back}, {self.edge_left_forward}, {self.edge_right_back}, {self.edge_right_forward}))'


class WingedEdgeShape(Drawable):
    __index = 1

    def __init__(self, name: str = None):
        self.name = name or f'shape_{self.__index}'
        self._vertices: dict[int, Vec3d] = {}
        self._adj_edges: List[Edge] = []
        self._adj_faces: List[int] = []
        self._adj_vertices: dict[int, int] = {}
        self._colors = []
        self.__printed = True

        self.__index += 1

    def draw(self, border=True):
        if not self.__printed:
            self.__eval__()

        for e_id in self._adj_faces:
            e = self._adj_edges[e_id]
            e_next: Edge = self._adj_edges[e.edge_left_forward]

            v1 = self._vertices[e.vert_origin]
            v2 = self._vertices[e.vert_dest]
            v3 = self._vertices[e_next.vert_dest]

            if not self.__printed:
                print(e_id, "=>", e)
                print(" ", "=>", v1, v2, v3)

            if border:
                # glEnable(GL_DEPTH_TEST)
                glLineWidth(2)
                glColor3f(*color.RED)
                glBegin(GL_LINE_STRIP)
                glVertex4f(*v1)
                glVertex4f(*v2)
                glVertex4f(*v3)
                glVertex4f(*v1)
                glEnd()
                # glDisable(GL_DEPTH_TEST)

            glColor3f(*color.GRAY)
            glBegin(GL_TRIANGLES)
            glVertex4f(*v1)
            glVertex4f(*v2)
            glVertex4f(*v3)
            glEnd()

        self.__printed = True

    def draw_border(self):
        pass

    def __getitem__(self, index: Union[int, slice]):
        pass

    def rotate(self, theta_0: float, theta_1: float, theta_2: float, order="xyz") -> None:
        pass

    def translate(self, tx: float, ty: float, tz: float) -> None:
        pass

    def scale(self, sx: float, sy: float, sz: float) -> None:
        pass

    def undo(self):
        pass

    def clone(self) -> 'WingedEdgeShape':
        pass

    def __str__(self) -> str:
        len_face = len(self._adj_faces)
        len_edge = len(self._adj_edges)
        len_vert = len(self._adj_vertices)
        return f'Shape(name={self.name}, faces={len_face}, edges={len_edge}, points={len_vert})'

    def __eval__(self):
        print("____________________________________________________\n")
        print("name:", self.name)
        print("____________________________________________________\n")

        print("v_id".ljust(25), "v")
        for v_id, v in self._vertices.items():
            print(str(v_id).ljust(25), v)

        print("____________________________________________________\n")

        print("f_id".ljust(5), "e_id")
        for f_id, e_id in enumerate(self._adj_faces):
            print(str(f_id).ljust(5), e_id)

        print("____________________________________________________\n")

        print("e_id".ljust(5), "e")
        for e_id, e in enumerate(self._adj_edges):
            v = f'{self._vertices.get(e.vert_origin)}, {self._vertices.get(e.vert_dest)}'
            f = f'{e.face_left}, {e.face_right}'
            e = f'{e.edge_left_back}, {e.edge_left_forward}, {e.edge_right_back}, {e.edge_right_forward}'
            print(str(e_id).ljust(5), f'Edge(v=({v}); f=({f}); e=({e}))')

        print("____________________________________________________\n")

        print("v_id".ljust(35), "e_id")
        for v_id, e_id in self._adj_vertices.items():
            print(str(self._vertices[v_id]).ljust(35), e_id)

        print("____________________________________________________\n")

    def add_tri(self,
                vertice0=Vec3d,
                vertice1=Vec3d,
                vertice2=Vec3d,
                color0: Tuple[int, int, int] = color.WHITE,
                color1: Tuple[int, int, int] = color.WHITE,
                color2: Tuple[int, int, int] = color.WHITE):

        h_v0 = hash(vertice0)
        h_v1 = hash(vertice1)
        h_v2 = hash(vertice2)

        self._vertices[h_v0] = vertice0
        self._vertices[h_v1] = vertice1
        self._vertices[h_v2] = vertice2

        f_index = len(self._adj_faces)

        e0_index = self._adj_vertices.get(h_v0)
        e0 = self._adj_edges[e0_index] if e0_index is not None else None

        e1_index = len(self._adj_edges)
        e2_index = e1_index + 1

        e1 = Edge()
        e1.set_vert(h_v1, h_v2)
        e1.set_face(f_index, None)
        e1.set_edge(e0_index,
                    e2_index,
                    self._adj_vertices.get(h_v1),
                    None)
        self._adj_edges.append(e1)

        e2 = Edge()
        e2.set_vert(h_v2, h_v0)
        e2.set_face(f_index, None)
        e2.set_edge(e1_index,
                    e0_index,
                    None,
                    self._adj_vertices.get(h_v0))
        self._adj_edges.append(e2)

        self._adj_faces.append(e1_index)

        self._adj_vertices[h_v2] = e1_index

        if e0 is not None:
            e0.set_edge_right(e1_index, e2_index)

    def add_quad(self,
                 vertice0=Vec3d,
                 vertice1=Vec3d,
                 vertice2=Vec3d,
                 vertice3=Vec3d,
                 color0: Tuple[int, int, int] = color.WHITE,
                 color1: Tuple[int, int, int] = color.WHITE,
                 color2: Tuple[int, int, int] = color.WHITE,
                 color3: Tuple[int, int, int] = color.WHITE):
        self.add_tri(vertice0, vertice1, vertice3,
                     color0, color1, color3)
        self.add_tri(vertice3, vertice1, vertice2,
                     color3, color1, color2)

    @ staticmethod
    def quadrilateral(
        vertice0=Vec3d,
        vertice1=Vec3d,
        vertice2=Vec3d,
        vertice3=Vec3d,
        color0: Tuple[int, int, int] = color.WHITE,
        color1: Tuple[int, int, int] = color.WHITE,
        color2: Tuple[int, int, int] = color.WHITE,
        color3: Tuple[int, int, int] = color.WHITE,
    ):
        obj = WingedEdgeShape()

        obj.add_quad(vertice0, vertice1, vertice2, vertice3,
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

        obj.add_tri(vertice0, vertice1, vertice2,
                    color0,   color1,   color2)

        return obj

        # h_v0 = hash(vertice0)
        # h_v1 = hash(vertice1)
        # h_v2 = hash(vertice2)

        # obj._vertices[h_v0] = vertice0
        # obj._vertices[h_v1] = vertice1
        # obj._vertices[h_v2] = vertice2

        # e0 = Edge()
        # e0.set_vert(h_v0, h_v1)
        # e0.set_face(0, None)
        # e0.set_edge(2, 1, None, None)
        # obj._adj_edges.append(e0)

        # e1 = Edge()
        # e1.set_vert(h_v1, h_v2)
        # e1.set_face(0, None)
        # e1.set_edge(0, 2, None, None)
        # obj._adj_edges.append(e1)

        # e2 = Edge()
        # e2.set_vert(h_v2, h_v0)
        # e2.set_face(0, None)
        # e2.set_edge(1, 0, None, None)
        # obj._adj_edges.append(e2)

        # obj._adj_faces.append(0)

        # obj._adj_vertices[h_v0] = 0
        # obj._adj_vertices[h_v1] = 1
        # obj._adj_vertices[h_v2] = 2

        # obj._colors.append(color0)
        # obj._colors.append(color1)
        # obj._colors.append(color2)

        # return obj
