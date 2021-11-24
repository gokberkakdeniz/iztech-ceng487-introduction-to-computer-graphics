# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from abc import ABC, abstractmethod


class Element(ABC):
    @abstractmethod
    def draw():
        pass

    @abstractmethod
    def draw_border():
        pass
