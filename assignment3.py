# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from math import pi
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from sys import argv
from os.path import basename

from lib.shape import Object3d
from lib.ui import create_ascii_table, create_ascii_table_header, BaseApplication
from lib.ui.elements import SubdivisionLevelElement, HelpButtonElement, HelpElement
from lib.ui.scene import Scene
from lib.utils.reader import parse_obj


class Assignment3Application(BaseApplication):
    def __init__(self, obj: Object3d, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.mouse_x = 0
        self.mouse_y = 0
        self.show_help = False

        # model scene
        self.scene_model = Scene()
        self.scene_model.register(obj)

        # model ui scene
        self.scene_ui = Scene()

        self.element_subdivision_level = SubdivisionLevelElement()
        self.scene_ui.register(self.element_subdivision_level)

        self.element_help_button = HelpButtonElement()
        self.scene_ui.register(self.element_help_button)

        # help ui scene
        self.scene_help = Scene(visible=False)

        self.element_help = HelpElement()
        self.scene_help.register(self.element_help)

    def draw_gl_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        level = str(self.scene_model.objects[0][0].level)
        self.element_subdivision_level.set_level(level)

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
            self.scene_model.objects[0][0].increase_subdivisions()
        elif key == b'-':
            self.scene_model.objects[0][0].decrease_subdivisions()

    def on_special_key_press(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.scene_model.objects[0][0].rotate(0, -pi/8, 0)
        elif key == GLUT_KEY_RIGHT:
            self.scene_model.objects[0][0].rotate(0, +pi/8, 0)
        elif key == GLUT_KEY_UP:
            self.scene_model.objects[0][0].rotate(-pi/8, 0, 0)
        elif key == GLUT_KEY_DOWN:
            self.scene_model.objects[0][0].rotate(+pi/8, 0, 0)

    def on_mouse_click(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_UP:
                width, height = self.size
                dx = (pi) * (y - self.mouse_y)/width
                dy = (pi) * (x - self.mouse_x)/height
                self.scene_model.objects[0][0].rotate(dy, dx, 0, "yxz")
            else:
                self.mouse_x = x
                self.mouse_y = y
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
            self.scene_model.objects[0][0].undo()
        elif button == GLUT_CURSOR_DESTROY and state == GLUT_UP:
            self.scene_model.objects[0][0].scale(1.5)
        elif button == GLUT_CURSOR_HELP and state == GLUT_UP:
            self.scene_model.objects[0][0].scale(0.75)

    # def on_mouse_drag(self, x, y):
    #     width, height = self.size
    #     dx = (pi) * (y - self.mouse_y)/width
    #     dy = (pi) * (x - self.mouse_x)/height
    #     self.scene_model.objects[0][0].rotate(dy, dx, 0, "yxz")
    #     self.mouse_x = x
    #     self.mouse_y = y

    def on_mouse_move(self, x, y):
        if 30 <= y <= 50 and 605 <= x <= 620:
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
    except FileNotFoundError:
        print("error: the given file does not exist.")
        exit(2)
    except Exception as e:
        print("error: could not parse the file.")
        print("      ", e)
        exit(3)

    app = Assignment3Application(
        obj,
        "IZTECH CENG487 - 10 2021 - 250201041 [" + basename(argv[1]) + "]",
        argv=argv[:2]
    )
    app.start()


if __name__ == "__main__":
    main()
