# CENG 487 Assignment2 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from math import pi
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from signal import signal, SIGINT
import sys

from lib.shape import Torus, Box, Cylinder, Sphere

"""
============================ CHANGELOG ============================

FEATURES
- Help text is moved to UI.
- Keep previous shapes in memory to preserve transformations and 
object recreation.
- Rotation around x/y axis with keyboard added.
- Object name drawn to screen.
- Object reset added (recreates).

FIXES
- Rotating with mouse drag is fixed.
- Torus linear edge is fixed.

IMPROVEMENTS
- Transformations are applied to master matrix too. This improves 
performance while changing subdivision count.Previous implementation 
had O(n) complexity (was applying each matrix in the stack to object) 
but this one recovers in O(1).
====================================================================
"""

primitives = [Sphere(), None, None, None]
primitives_index = 0
primitive = primitives[primitives_index]
mouse_x = 0
mouse_y = 0
show_help = False


def build_options(options):
    return ("\n".join(map(lambda option: option[0].ljust(20) + option[1], options)) + "\n\n").encode("utf-8")


objects_text = build_options([
    ("1",     "sphere"),
    ("2",     "box"),
    ("3",     "cylinder"),
    ("4",     "torus"),
])
transformation_text = build_options([
    ("MWHEELUP",     "zoom in"),
    ("MWHEELDOWN",   "zoom out"),
    ("MRIGHT",       "undo last transformation"),
    ("LEFTARROW",    "rotate around y axis (cw)"),
    ("RIGHTARROW",   "rotate around y axis (ccw)"),
    ("UPARROW",      "rotate around x axis (cw)"),
    ("DOWNARROW",    "rotate around x axis (ccw)"),
    ("MLEFT",        "(drag and drop) rotate"),
    ("R",            "reset object"),
])
quality_text = build_options([
    ("+",     "increase subdivision count"),
    ("-",     "decrease subdivision count"),
])


def draw_help_text():
    glColor3f(0.0, 1.0, 1.0)
    glRasterPos2i(-1, 2)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'KEYBOARD SHORTCUTS')

    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2i(-3, 2)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'\nOBJECTS\n')
    glutBitmapString(GLUT_BITMAP_9_BY_15, objects_text)

    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'QUALITY\n')
    glutBitmapString(GLUT_BITMAP_9_BY_15, quality_text)

    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'TRANSFORMATION\n')
    glutBitmapString(GLUT_BITMAP_9_BY_15, transformation_text)


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


def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene():
    object_name = primitive.__class__.__name__

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6.0)
    glutSetWindowTitle(f"IZTECH CENG487 - 10 2021 - 250201041 [{object_name}]")

    if show_help:
        draw_help_text()
    else:
        primitive.draw_border()
        primitive.draw()

        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2i(-3, -2)
        glutBitmapString(GLUT_BITMAP_9_BY_15, object_name.encode("utf-8"))

    glColor3f(0.0, 1.0, 1.0)
    glRasterPos2i(3, 2)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'?')

    glutSwapBuffers()


def keyboardFunc(key, x, y):
    global primitive, primitives_index

    if ord(key) == 27:
        glutLeaveMainLoop()
    elif key == b'1':
        primitives_index = 0
        primitives[primitives_index] = primitives[primitives_index] or Sphere()
        primitive = primitives[primitives_index]
    elif key == b'2':
        primitives_index = 1
        primitives[primitives_index] = primitives[primitives_index] or Box()
        primitive = primitives[primitives_index]
    elif key == b'3':
        primitives_index = 2
        primitives[primitives_index] = primitives[primitives_index] or Cylinder()
        primitive = primitives[primitives_index]
    elif key == b'4':
        primitives_index = 3
        primitives[primitives_index] = primitives[primitives_index] or Torus()
        primitive = primitives[primitives_index]
    elif key == b'+':
        primitive.increase_subdivisions()
    elif key == b'-':
        primitive.decrease_subdivisions()
    elif key == b'r':
        primitives[primitives_index] = primitives[primitives_index].__class__()
        primitive = primitives[primitives_index]


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


def passiveMotionFunc(x, y):
    global show_help

    if 30 <= y <= 50 and 605 <= x <= 620:
        glutSetCursor(GLUT_CURSOR_INFO)
        show_help = True
    else:
        glutSetCursor(GLUT_CURSOR_INHERIT)
        show_help = False


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


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)

    glutCreateWindow("IZTECH CENG487 - 10 2021 - 250201041")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyboardFunc)
    glutMouseFunc(mouseFunc)
    glutSpecialFunc(specialFunc)
    glutPassiveMotionFunc(passiveMotionFunc)
    InitGL(640, 480)

    signal(SIGINT, lambda *_: glutLeaveMainLoop())

    glutMainLoop()


if __name__ == "__main__":
    main()
