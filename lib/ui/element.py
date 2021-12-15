# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from ..shape import Drawable


class Element(Drawable):
    def __init__(self) -> 'Element':
        self.pos = (0, 0)

    def set_pos(self, pos):
        self.pos = pos
