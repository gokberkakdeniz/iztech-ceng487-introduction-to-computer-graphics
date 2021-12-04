# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from math import pi
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from sys import argv
from os.path import basename
from lib.math.vector import Vec3d

from lib.shape import Object3d, color, WingedEdgeShape
from lib.shape.shape import Shape
from lib.ui import BaseApplication, Camera, Scene
from lib.ui.elements import SubdivisionLevelElement, HelpButtonElement, HelpElement
from lib.utils.reader import parse_obj


class Assignment4Application(BaseApplication):
    def __init__(self, obj: Shape, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.mouse_x = 0
        self.mouse_y = 0
        self.show_help = False

        self.camera_model = Camera()
        self.camera_ui = Camera()

        # model scene
        self.scene_model = Scene(cameras=(self.camera_model,))
        self.scene_model.register(obj)

        # model ui scene
        self.scene_ui = Scene(cameras=(self.camera_ui,))

        self.element_subdivision_level = SubdivisionLevelElement()
        self.scene_ui.register(self.element_subdivision_level)

        self.element_help_button = HelpButtonElement()
        self.scene_ui.register(self.element_help_button)

        # help ui scene
        self.scene_help = Scene(cameras=(self.camera_ui,), visible=False)

        self.element_help = HelpElement()
        self.scene_help.register(self.element_help)

    def draw_gl_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # level = self.scene_model.objects[0][0].level
        # self.element_subdivision_level.set_level(level)
        self.element_help_button.set_pos((self.size[0]-30, self.size[1]-30))

        self.scene_ui.draw()
        self.scene_help.draw()
        self.scene_model.draw()

        glutSwapBuffers()

    def on_display(self):
        return self.draw_gl_scene()

    def on_idle(self):
        return self.draw_gl_scene()

    def on_key_press(self, key, x, y):
        super().on_key_press(key, x, y)

        if key == b'+':
            for obj in self.scene_model.objects:
                obj[0].increase_subdivisions()
        elif key == b'-':
            for obj in self.scene_model.objects:
                obj[0].decrease_subdivisions()
        elif key == b'r':
            self.scene_model.active_camera.reset()

    def on_special_key_press(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.scene_model.active_camera.rotate(0, -pi/8, 0)
        elif key == GLUT_KEY_RIGHT:
            self.scene_model.active_camera.rotate(0, +pi/8, 0)
        elif key == GLUT_KEY_UP:
            self.scene_model.active_camera.rotate(-pi/8, 0, 0)
        elif key == GLUT_KEY_DOWN:
            self.scene_model.active_camera.rotate(+pi/8, 0, 0)

    def on_mouse_click(self, button, state, x, y):
        if button == GLUT_CURSOR_DESTROY and state == GLUT_UP:
            self.scene_model.active_camera.zoom_in()
        elif button == GLUT_CURSOR_HELP and state == GLUT_UP:
            self.scene_model.active_camera.zoom_out()

    def on_mouse_drag(self, x, y):
        width, height = self.size

        dx = (pi/2) * (y - self.mouse_y)/width
        dy = (pi/2) * (x - self.mouse_x)/height

        self.mouse_x = x
        self.mouse_y = y

        self.scene_model.active_camera.rotate(dy, dx, 0)

    def on_mouse_move(self, x, y):
        if y < 30 and x > self.size[0] - 30:
            glutSetCursor(GLUT_CURSOR_INFO)
            self.scene_help.set_visibility(True)
            self.scene_ui.set_visibility(False)
            self.scene_model.set_visibility(False)
        else:
            glutSetCursor(GLUT_CURSOR_INHERIT)
            self.scene_help.set_visibility(False)
            self.scene_ui.set_visibility(True)
            self.scene_model.set_visibility(True)


def main():
    argc = len(argv)
    obj = None

    if argc < 2:
        print("error: object file must be given.")
        exit(1)

    try:
        obj = parse_obj(argv[1])
        # obj = WingedEdgeShape.triangle(
        #     Vec3d.point(0, 0, 0), Vec3d.point(0, -1, 0), Vec3d.point(1, 0, 0),
        #     color.GRAY,
        #     color.GRAY,
        #     color.GRAY,
        # )
        # obj = WingedEdgeShape.quadrilateral(
        #     Vec3d.point(0, 0, 0),
        #     Vec3d.point(0, -1, 0),
        #     Vec3d.point(1, -1, 0),
        #     Vec3d.point(1, 0, 0),
        #     color.GRAY,
        #     color.GRAY,
        #     color.GRAY,
        #     color.GRAY,
        # )
        # obj = WingedEdgeShape()
        # obj.add_face(
        #     Vec3d.point(0, 0, 0),
        #     Vec3d.point(0, -1, 0),
        #     Vec3d.point(1, 0, 0),
        #     color.GRAY,
        #     color.GRAY,
        #     color.GRAY,
        # )
        # obj.add_face(
        #     Vec3d.point(1, 0, 0),
        #     Vec3d.point(0, -1, 0),
        #     Vec3d.point(1, -1, 0),
        #     color.GRAY,
        #     color.GRAY,
        #     color.GRAY,
        # )
        # obj.add_face(
        #     Vec3d.point(1, 0, 0),
        #     Vec3d.point(1, -1, 0),
        #     Vec3d.point(1.5, -0.5, 0),
        #     color.GRAY,
        #     color.GRAY,
        #     color.GRAY,
        # )
    except FileNotFoundError:
        print("error: the given file does not exist.")
        exit(2)
    except Exception as e:
        print("error: could not parse the file.")
        raise e

    app = Assignment4Application(
        obj,
        "IZTECH CENG487 - 12 2021 - 250201041 [" + basename(argv[1]) + "]",
        argv=argv[:2]
    )
    app.start()


if __name__ == "__main__":
    main()
