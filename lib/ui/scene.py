# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from typing import Iterable, List, Tuple

from lib.shape.light import Light
from lib.shape.shader import Resource
from ..shape import WingedEdgeShape, Camera


class Scene:
    def __init__(self,
                 cameras: Iterable[Camera],
                 lights: Iterable[Light] = [],
                 resources: Iterable[Resource] = [],
                 visible=True) -> None:
        self.objects: List[Tuple[WingedEdgeShape, bool]] = []
        self.cameras = list(cameras)
        self.active_camera = self.cameras[0]
        self.lights = list(lights)
        self.resources = list(resources)
        self.visible = visible
        self.mode_border = False
        self.mode_background = True

    def set_visibility(self, visible: bool):
        self.visible = visible

    def get_visibility(self):
        return self.visible

    def set_mode(self, background: bool = None, border: bool = None):
        if background is not None:
            self.mode_background = background
        if border is not None:
            self.mode_border = border

    def set_visibility_of(self, element: WingedEdgeShape, visible: bool) -> bool:
        for i in range(len(self.objects)):
            obj = self.objects[i]

            if obj[0] == element:
                obj[1] = visible
                return True

        return False

    def get_visibility_of(self, element: WingedEdgeShape) -> bool:
        for i in range(len(self.objects)):
            obj = self.objects[i]

            if obj[0] == element:
                return obj[1]

        return None

    def register(self, obj: WingedEdgeShape, visible=True):
        self.objects.append([obj, visible])

    def unregister(self, element: WingedEdgeShape) -> bool:
        for i in range(len(self.objects)):
            if self.objects[i][0] == element:
                del self.objects[i]

                return True

        return False

    def draw(self):
        if self.visible:
            self.active_camera.load()

            for res in self.resources+self.lights:
                if res.should_reload():
                    print(res)
                    res.load()

            for el in self.objects:
                obj, visible = el

                if visible:
                    obj.draw(background=self.mode_background,  border=self.mode_border)
