# CENG 487 Assignment7 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw(self, border=True, background=True):
        pass
