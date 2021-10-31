
from abc import ABC, abstractmethod
from typing import List
from .shape import Shape


class Object3d(ABC):
    def __init__(self, subdivisions: List[Shape]) -> None:
        super().__init__()
        self.subdivisions = subdivisions

    @abstractmethod
    def increase_subdivisions(self):
        pass

    @abstractmethod
    def decrease_subdivisions(self):
        pass

    def draw(self):
        for division in self.subdivisions:
            division.draw()

    def draw_border(self):
        for division in self.subdivisions:
            division.draw_border()
