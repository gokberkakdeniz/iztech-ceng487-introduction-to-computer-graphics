# CENG 487 Assignment5 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import Union


class WingedEdge:
    def __init__(self) -> None:
        self.vert_origin = None
        self.vert_dest = None

        self.face_left = None
        self.face_right = None

        self.edge_left_back = None
        self.edge_left_forward = None
        self.edge_right_back = None
        self.edge_right_forward = None

    def set_vert(self,
                 origin: Union[int, None],
                 dest: Union[int, None]):
        self.vert_origin = origin
        self.vert_dest = dest

    def set_face(self, left:
                 Union[int, None],
                 right: Union[int, None]):
        self.face_left = left
        self.face_right = right

    def set_edge(self,
                 left_back: Union[int, None],
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
        v = f'{self.vert_origin}, {self.vert_dest}'
        f = f'{self.face_left}, {self.face_right}'
        e = f'{self.edge_left_back}, {self.edge_left_forward}, {self.edge_right_back}, {self.edge_right_forward}'

        return f'Edge(v=({v}); f=({f}); e=({e}))'

    def __hash__(self) -> int:
        return hash((self.vert_origin, self.vert_dest))
