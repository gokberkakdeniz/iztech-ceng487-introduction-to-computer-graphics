# CENG 487 Assignment7 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from abc import ABC, abstractmethod
from . import Drawable


class Shape(Drawable, ABC):
    @abstractmethod
    def draw(self, border=True, background=True):
        pass

    @abstractmethod
    def rotate(self, theta_0: float, theta_1: float, theta_2: float, order="xyz") -> None:
        pass

    @abstractmethod
    def translate(self, tx: float, ty: float, tz: float) -> None:
        pass

    @abstractmethod
    def scale(self, sx: float, sy: float, sz: float) -> None:
        pass

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def clone(self) -> 'Shape':
        pass
