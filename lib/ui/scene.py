# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from typing import Iterable, List, Set, Tuple, Union
from ..shape import Shape, Object3d
from .camera import Camera


class Scene:
    def __init__(self, cameras: Iterable[Camera], visible=True) -> None:
        self.objects: List[Tuple[Union[Shape, Object3d], bool]] = []
        self.cameras: Set[Camera] = list(cameras)
        self.active_camera = self.cameras[0]
        self.visible = visible

    def set_visibility(self, visible: bool):
        self.visible = visible

    def set_visibility_of(self, element: Union[Shape, Object3d], visible: bool) -> bool:
        for i in range(len(self.objects)):
            obj = self.objects[i]

            if obj[0] == element:
                obj[1] = visible
                return True

        return False

    def register(self, obj: Union[Shape, Object3d], visible=True):
        self.objects.append([obj, visible])

    def unregister(self, element: Union[Shape, Object3d]) -> bool:
        for i in range(len(self.objects)):
            if self.objects[i][0] == element:
                del self.objects[i]

                return True

        return False

    def draw(self, border=True):
        self.active_camera.look()
        if self.visible:
            for el in self.objects:
                obj, visible = el

                if visible:
                    if border:
                        obj.draw_border()

                    obj.draw()
