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
from lib.utils.reader import parse_obj


class Assignment3Application(BaseApplication):
    def __init__(self, obj: Object3d, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.object = obj
        self.mouse_x = 0
        self.mouse_y = 0
        self.show_help = False

    def draw_gl_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -6.0)

        if self.show_help:
            self.draw_help_text()
        else:
            self.object.draw_border()
            self.object.draw()
            self.draw_subdivision_level()

        self.draw_help_button()

        glutSwapBuffers()

    def on_display(self):
        return self.draw_gl_scene()

    def on_idle(self):
        return self.draw_gl_scene()

    def on_key_press(self, key, x, y):
        super().on_key_press(key, x, y)

        if key == b'+':
            self.object.increase_subdivisions()
        elif key == b'-':
            self.object.decrease_subdivisions()

    def on_special_key_press(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.object.rotate(0, -pi/8, 0)
        elif key == GLUT_KEY_RIGHT:
            self.object.rotate(0, +pi/8, 0)
        elif key == GLUT_KEY_UP:
            self.object.rotate(-pi/8, 0, 0)
        elif key == GLUT_KEY_DOWN:
            self.object.rotate(+pi/8, 0, 0)

    def on_mouse_click(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_UP:
                width, height = self.size
                dx = (pi) * (y - self.mouse_y)/width
                dy = (pi) * (x - self.mouse_x)/height
                self.object.rotate(dy, dx, 0, "yxz")
            else:
                self.mouse_x = x
                self.mouse_y = y
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
            self.object.undo()
        elif button == GLUT_CURSOR_DESTROY and state == GLUT_UP:
            self.object.scale(1.5)
        elif button == GLUT_CURSOR_HELP and state == GLUT_UP:
            self.object.scale(0.75)

    def on_mouse_drag(self, x, y):
        width, height = self.size
        dx = (pi) * (y - self.mouse_y)/width
        dy = (pi) * (x - self.mouse_x)/height
        self.object.rotate(dy, dx, 0, "yxz")
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_move(self, x, y):
        if 30 <= y <= 50 and 605 <= x <= 620:
            glutSetCursor(GLUT_CURSOR_INFO)
            self.show_help = True
        else:
            glutSetCursor(GLUT_CURSOR_INHERIT)
            self.show_help = False

    def draw_subdivision_level(self):
        glColor3f(0.0, 1.0, 1.0)
        glRasterPos2i(-3, -2)
        glutBitmapString(GLUT_BITMAP_9_BY_15,
                         str(self.object.level).encode("utf-8"))

    def draw_help_button(self):
        glColor3f(0.0, 1.0, 1.0)
        glRasterPos2i(3, 2)
        glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'?')

    def draw_help_text(self):
        glColor3f(0.0, 1.0, 1.0)
        glRasterPos2i(-1, 2)
        self.draw_keyboard_shortcuts_title()

        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2i(-3, 2)

        self.draw_quality_title()
        self.draw_quality_table()

        self.draw_transformation_title()
        self.draw_transformation_table()

    draw_keyboard_shortcuts_title = staticmethod(
        create_ascii_table_header("keyboard shortcuts")
    )
    draw_quality_title = staticmethod(
        create_ascii_table_header("\nquality")
    )
    draw_quality_table = staticmethod(
        create_ascii_table([
            ("+", "increase subdivision count"),
            ("-", "decrease subdivision count"),
        ])
    )
    draw_transformation_title = staticmethod(
        create_ascii_table_header("transformation")
    )
    draw_transformation_table = staticmethod(
        create_ascii_table([
            ("MWHEELUP",     "zoom in"),
            ("MWHEELDOWN",   "zoom out"),
            ("MLEFT",        "rotate (drag and drop)"),
            ("MRIGHT",       "undo last transformation"),
            ("LEFTARROW",    "rotate around y axis (cw)"),
            ("RIGHTARROW",   "rotate around y axis (ccw)"),
            ("UPARROW",      "rotate around x axis (cw)"),
            ("DOWNARROW",    "rotate around x axis (ccw)"),
            ("R",            "reset object"),
        ])
    )


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
