# CENG 487 Assignment5 by
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
from lib.shape import WingedEdgeShape,  Grid, Shader
from lib.shape.shader import Program
from lib.ui import BaseApplication, Camera, Scene
from lib.ui.elements import StatisticsElement, HelpButtonElement, HelpElement
from lib.utils.reader import parse_obj


class Assignment5Application(BaseApplication):
    def __init__(self, objs: List[WingedEdgeShape], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.mouse_x = 0
        self.mouse_y = 0
        self.show_help = False
        self.rerender = False

        self.camera_model = Camera()
        self.camera_model.zoom_out(0.4)
        self.camera_model.rotate(pi/4, pi/8, 0)
        self.camera_ui = Camera()

        # model scene
        self.scene_model = Scene(cameras=(self.camera_model,))
        self.element_grid = Grid((10, 10))
        self.scene_model.register(self.element_grid)

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
        program = Program([
            Shader(join(root, "shaders", "model.frag")),
            Shader(join(root, "shaders", "model.vert"))
        ])

        for obj, _ in self.scene_model.objects:
            obj.use_program(program)

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
            print("======== Catmull Clark Subdivision ========")
            for obj in self.scene_model.objects[1:]:
                if hasattr(obj[0], "subdivide_catmull_clark"):
                    start_time = time()
                    obj[0].subdivide_catmull_clark()
                    level = obj[0].level
                    time_diff = time() - start_time
                    if level > 0:
                        print(f' {obj[0].name:20s}\tL{level}\t{time_diff:.2f}s')
            print("===========================================\n")
            self.__recalculate_stats()
        elif key == b'-':
            for obj in self.scene_model.objects[1:]:
                if hasattr(obj[0], "reverse_subdivide_catmull_clark"):
                    obj[0].reverse_subdivide_catmull_clark()
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
        f_count, v_count, level = 0, 0, 0
        for obj, _ in self.scene_model.objects:
            f_count += len(obj._adj_faces)
            v_count += len(obj._adj_vertices)
            level = max(obj.level, level)
        self.element_stats.set_face_count(f_count)
        self.element_stats.set_vertice_count(v_count)
        self.element_stats.set_level(level)


def main():
    argc = len(argv)
    objs = []

    if argc < 2:
        print("info: no file given, loading defaults...")

        root = dirname(__file__)

        print("info: loading ecube.obj")
        ecube = parse_obj(join(root, "assets", "ecube.obj"))
        print("info: cloning ecube.obj")
        ecube2 = ecube.clone()
        ecube2.name += "2"
        ecube.scale(1.1, 1.1, 1.1)
        ecube.translate(4, 1.1, 0)
        objs.append(ecube)

        ecube2.rotate(pi/4, 0, pi/4)
        ecube2.scale(0.5, 0.5, 0.5)
        ecube2.translate(4, 4, 0)
        objs.append(ecube2)

        print("info: loading tori.obj")
        tori = parse_obj(join(root, "assets", "tori.obj"))
        tori.scale(1.1, 1.1, 1.1)
        tori.translate(-1.5, 1.1, 0)
        objs.append(tori)

        print("info: loading humanoid_quad.obj")
        humanoid_quad = parse_obj(join(root, "assets", "humanoid_quad.obj"))
        humanoid_quad.rotate(-pi/2, 0, 0)
        humanoid_quad.translate(-2.5, -0.5, +4)
        objs.append(humanoid_quad)

        print("info: loading sphere.obj")
        sphere = parse_obj(join(root, "assets", "sphere.obj"))
        sphere.translate(+3.5, 3.5, -3.5)
        sphere.max_level = 0
        objs.append(sphere)

        print("info: loading violin_case.obj")
        violin_case = parse_obj(join(root, "assets", "violin_case.obj"))
        violin_case.translate(+2, 0, +3)
        violin_case.max_level = 0
        objs.append(violin_case)

    else:
        try:
            print(f'info: loading "{argv[1]}"...')

            objs.append(parse_obj(argv[1]))

            print(f'info: "{argv[1]}" loaded.')
        except FileNotFoundError:
            print("error: the given file does not exist.")
            exit(2)
        except Exception as e:
            print("error: could not parse the file.")
            raise e

    obj_names = ", ".join(map(lambda o: o.name, objs))
    app = Assignment5Application(
        objs,
        "IZTECH CENG487 - 12 2021 - 250201041 [" + obj_names + "]",
        argv=argv[:2]
    )
    app.start()


if __name__ == "__main__":
    main()
