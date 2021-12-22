# CENG 487 Assignment5 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .. import create_ascii_table, create_ascii_table_header, Element


class HelpElement(Element):
    def draw(self, background=None, border=None):
        glColor3f(0.0, 1.0, 1.0)
        glWindowPos2f(*self.pos)
        self.draw_keyboard_shortcuts_title()

        glColor3f(1.0, 1.0, 1.0)
        glWindowPos2f(self.pos[0], self.pos[1] - 30)

        self.draw_quality_title()
        self.draw_quality_table()

        self.draw_camera_title()
        self.draw_camera_table()

        self.draw_drawing_title()
        self.draw_drawing_table()

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
    draw_camera_title = staticmethod(
        create_ascii_table_header("camera")
    )
    draw_camera_table = staticmethod(
        create_ascii_table([
            ("MWHEELUP",     "zoom in"),
            ("MWHEELDOWN",   "zoom out"),
            ("MLEFT",        "rotate (drag and drop)"),
            ("LEFTARROW",    "rotate around y axis (cw)"),
            ("RIGHTARROW",   "rotate around y axis (ccw)"),
            ("UPARROW",      "rotate around x axis (cw)"),
            ("DOWNARROW",    "rotate around x axis (ccw)"),
            ("R",            "reset object"),
        ])
    )
    draw_drawing_title = staticmethod(
        create_ascii_table_header("drawing")
    )
    draw_drawing_table = staticmethod(
        create_ascii_table([
            ("S", "toggle background drawing "),
            ("E", "toggle border drawing "),
            ("G", "toggle grid "),
        ])
    )
