# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw():
        pass

    @abstractmethod
    def draw_border():
        pass
