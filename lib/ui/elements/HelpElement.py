# CENG 487 Assignment3 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .. import create_ascii_table, create_ascii_table_header, Element


class HelpElement(Element):
    def __init__(self) -> None:
        super().__init__()

    def draw(self):
        glColor3f(0.0, 1.0, 1.0)
        glRasterPos2i(-1, 2)
        self.draw_keyboard_shortcuts_title()

        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2i(-3, 2)

        self.draw_quality_title()
        self.draw_quality_table()

        self.draw_transformation_title()
        self.draw_transformation_table()

    def draw_border(self):
        pass

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
