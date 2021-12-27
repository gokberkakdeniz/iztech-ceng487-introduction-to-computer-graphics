# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from math import pi
from typing import List
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from sys import argv
from os.path import join, dirname
from time import time
from lib.math.vector import Vec3d
from lib.shape import WingedEdgeShape, Grid, Shader, Camera, Program, TextureBlender, DirectionalLight, PointLight
from lib.shape.color import RGBA
from lib.ui import BaseApplication, Scene
from lib.ui.elements import StatisticsElement, HelpButtonElement, HelpElement
from lib.utils.reader import parse_obj


class Assignment6Application(BaseApplication):
    def __init__(self, objs: List[WingedEdgeShape], *args, **kwargs) -> None:
        super().__init__(size=(800, 600), *args, **kwargs)

        self.mouse_x = 0
        self.mouse_y = 0
        self.show_help = False
        self.rerender = False

        self.camera_model = Camera()
        self.camera_ui = Camera()

        self.texture_blender = TextureBlender()

        self.light1 = PointLight(Vec3d.point(0, 1.6023981999999999, 0), RGBA.white())
        self.light2 = DirectionalLight(Vec3d.vector(1, 0, 0), RGBA.blue())

        # model scene
        self.scene_model = Scene(
            cameras=(self.camera_model,),
            resources=(self.texture_blender,),
            lights=(self.light1, self.light2)
        )
        self.element_grid = Grid((50, 50))
        self.scene_model.register(self.element_grid)
        self.scene_model.set_visibility_of(self.element_grid, False)

        for obj in objs:
            self.scene_model.register(obj)

        # model ui scene
        self.scene_ui = Scene(cameras=(self.camera_ui,))

        self.element_stats = StatisticsElement()
        self.__recalculate_stats()
        self.scene_ui.register(self.element_stats)

        self.element_help_button = HelpButtonElement()
        self.scene_ui.register(self.element_help_button)

        # help ui scene
        self.scene_help = Scene(cameras=(self.camera_ui,), visible=False)

        self.element_help = HelpElement()
        self.scene_help.register(self.element_help)

    def init_gl(self):
        super().init_gl()

        root = dirname(__file__)
        Program(
            shaders=[
                Shader(join(root, "shaders", "model.frag")),
                Shader(join(root, "shaders", "model.vert"))
            ],
            resources=[
                *self.scene_model.cameras,
                *[obj for obj, _ in self.scene_model.objects],
                self.texture_blender,
                self.light1,
                self.light2
            ]
        )

    def on_resize(self, width, height):
        super().on_resize(width, height)

        self.element_help_button.set_pos((self.size[0]-30, self.size[1]-30))
        self.element_help.set_pos((30, self.size[1]-40))
        self.camera_model.aspect = self.size[0] / self.size[1]
        self.camera_ui = self.size[0] / self.size[1]

    def draw_gl_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.scene_ui.draw()
        self.scene_help.draw()
        self.scene_model.draw()

        glutSwapBuffers()

    def on_display(self):
        return self.draw_gl_scene()

    def on_idle(self):
        if self.rerender:
            self.rerender = False
            return self.draw_gl_scene()

    def on_key_press(self, key, x, y):
        super().on_key_press(key, x, y)

        if key == b'+':
            self.texture_blender.increase()
            self.__recalculate_stats()
        elif key == b'-':
            self.texture_blender.decrease()
            self.__recalculate_stats()
        elif key == b'r':
            self.scene_model.active_camera.reset()
        elif key == b's':
            self.scene_model.set_mode(background=not self.scene_model.mode_background)
        elif key == b'e':
            self.scene_model.set_mode(border=not self.scene_model.mode_border)
        elif key == b'g':
            self.scene_model.set_visibility_of(self.element_grid,
                                               not self.scene_model.get_visibility_of(self.element_grid))
        elif key == b'1':
            self.light1.toogle()
            self.__recalculate_stats()
        elif key == b'2':
            self.light2.toogle()
            self.__recalculate_stats()
        elif key == b'a':
            print("a")

        self.mouse_x = x
        self.mouse_y = y
        self.rerender = True

    def on_special_key_press(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.scene_model.active_camera.rotate(0, -pi/8, 0)
        elif key == GLUT_KEY_RIGHT:
            self.scene_model.active_camera.rotate(0, +pi/8, 0)
        elif key == GLUT_KEY_UP:
            self.scene_model.active_camera.rotate(-pi/8, 0, 0)
        elif key == GLUT_KEY_DOWN:
            self.scene_model.active_camera.rotate(+pi/8, 0, 0)

        self.mouse_x = x
        self.mouse_y = y
        self.rerender = True

    def on_mouse_click(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP \
            and y < 30 and x > self.size[0] - 30 \
                and not self.scene_help.get_visibility():
            self.scene_help.set_visibility(True)
            self.scene_ui.set_visibility(False)
            self.scene_model.set_visibility(False)
        elif button == GLUT_CURSOR_DESTROY and state == GLUT_UP:
            self.scene_model.active_camera.zoom_in()
        elif button == GLUT_CURSOR_HELP and state == GLUT_UP:
            self.scene_model.active_camera.zoom_out()
        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP and self.scene_help.get_visibility():
            self.scene_help.set_visibility(False)
            self.scene_ui.set_visibility(True)
            self.scene_model.set_visibility(True)
        self.mouse_x = x
        self.mouse_y = y
        self.rerender = True

    def on_mouse_drag(self, x, y):
        dx = 0.005 * (y - self.mouse_y)
        dy = 0.005 * (x - self.mouse_x)

        self.scene_model.active_camera.rotate(dx, dy, 0)

        self.mouse_x = x
        self.mouse_y = y
        self.rerender = True

    def on_mouse_move(self, x, y):
        if not self.scene_help.get_visibility():
            if y < 30 and x > self.size[0] - 30:
                glutSetCursor(GLUT_CURSOR_INFO)
            else:
                glutSetCursor(GLUT_CURSOR_INHERIT)

    def __recalculate_stats(self):
        f_count, v_count, ratio = 0, 0, self.texture_blender.ratio
        for obj, _ in self.scene_model.objects:
            f_count += len(obj._adj_faces)
            v_count += len(obj._adj_vertices)

        self.element_stats.set_face_count(f_count)
        self.element_stats.set_vertice_count(v_count)
        self.element_stats.set_ratio(ratio)
        self.element_stats.set_light1(self.light1.is_open())
        self.element_stats.set_light2(self.light2.is_open())


def main():
    argc = len(argv)
    objs = []

    if argc < 2:
        print("error: please pass obj file as an argument.")
        exit(1)
    else:
        try:
            print(f'info: loading "{argv[1]}"...')

            objs.extend(parse_obj(argv[1]))

            print(f'info: "{argv[1]}" loaded.')
        except FileNotFoundError:
            print("error: the given file does not exist.")
            exit(2)
        except Exception as e:
            print("error: could not parse the file.")
            raise e

    app = Assignment6Application(
        objs,
        "IZTECH CENG487 - 12 2021 - 250201041 [" + argv[1] + "]",
        argv=argv[:2]
    )
    app.start()


if __name__ == "__main__":
    main()
