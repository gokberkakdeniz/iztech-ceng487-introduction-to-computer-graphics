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
from lib.shape.object3d import Object3d
from lib.ui import create_ascii_table
from lib.ui.text import create_ascii_table_header
from lib.utils.reader import parse_obj

primitive: Object3d = None

mouse_x = 0
mouse_y = 0
show_help = False

draw_keyboard_shortcuts_title = create_ascii_table_header("keyboard shortcuts")

draw_quality_title = create_ascii_table_header("\nquality")
draw_quality_table = create_ascii_table([
    ("+",            "increase subdivision count"),
    ("-",            "decrease subdivision count"),
])

draw_transformation_title = create_ascii_table_header("transformation")
draw_transformation_table = create_ascii_table([
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


def draw_help_text():
    glColor3f(0.0, 1.0, 1.0)
    glRasterPos2i(-1, 2)
    draw_keyboard_shortcuts_title()

    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2i(-3, 2)

    draw_quality_title()
    draw_quality_table()

    draw_transformation_title()
    draw_transformation_table()


def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(width, height):
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6.0)

    if show_help:
        draw_help_text()
    else:
        primitive.draw_border()
        primitive.draw()

        glColor3f(0.0, 1.0, 1.0)
        glRasterPos2i(-3, -2)

        level = str(primitive.level).encode("utf-8")
        glutBitmapString(GLUT_BITMAP_9_BY_15, level)

    glColor3f(0.0, 1.0, 1.0)
    glRasterPos2i(3, 2)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'?')

    glutSwapBuffers()


def keyboardFunc(key, x, y):
    global primitive

    if ord(key) == 27:
        glutLeaveMainLoop()
    elif key == b'+':
        primitive.increase_subdivisions()
    elif key == b'-':
        primitive.decrease_subdivisions()


def specialFunc(key, x, y):
    global primitive

    if key == GLUT_KEY_LEFT:
        primitive.rotate(0, -pi/8, 0)
    elif key == GLUT_KEY_RIGHT:
        primitive.rotate(0, +pi/8, 0)
    elif key == GLUT_KEY_UP:
        primitive.rotate(-pi/8, 0, 0)
    elif key == GLUT_KEY_DOWN:
        primitive.rotate(+pi/8, 0, 0)


def mouseFunc(button, state, x, y):
    global mouse_x, mouse_y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:
            dx = (pi) * (y - mouse_y)/640
            dy = (pi) * (x - mouse_x)/480
            primitive.rotate(dy, 0, dx, "yzx")
        else:
            mouse_x = x
            mouse_y = y
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        primitive.undo()
    elif button == GLUT_CURSOR_DESTROY and state == GLUT_UP:
        primitive.scale(1.5)
    elif button == GLUT_CURSOR_HELP and state == GLUT_UP:
        primitive.scale(0.75)


def passiveMotionFunc(x, y):
    global show_help

    if 30 <= y <= 50 and 605 <= x <= 620:
        glutSetCursor(GLUT_CURSOR_INFO)
        show_help = True
    else:
        glutSetCursor(GLUT_CURSOR_INHERIT)
        show_help = False


def main():
    global primitive
    argc = len(argv)

    if argc < 2:
        print("error: object file must be given.")
        exit(1)
    try:
        primitive = parse_obj(argv[1])
    except FileNotFoundError:
        print("error: the given file does not exist.")
        exit(2)

    glutInit(argv[2:])

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)

    glutCreateWindow(
        "IZTECH CENG487 - 10 2021 - 250201041 [" + basename(argv[1]) + "]"
    )
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyboardFunc)
    glutSpecialFunc(specialFunc)
    glutMouseFunc(mouseFunc)
    glutPassiveMotionFunc(passiveMotionFunc)
    InitGL(640, 480)
    glutMainLoop()


if __name__ == "__main__":
    main()
