# CENG 487 Assignment2 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from math import pi
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from sys import argv

from lib.shape.object3d import Object3d
from lib.utils.reader import parse_obj

primitive: Object3d = None

mouse_x = 0
mouse_y = 0


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

    primitive.draw_border()
    primitive.draw()

    glRasterPos2i(-3, -2)
    glColor4f(0.0, 0.0, 1.0, 1.0)
    glutBitmapString(GLUT_BITMAP_9_BY_15, str(primitive.level).encode("utf-8"))

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
    if button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        primitive.undo()
    elif button == GLUT_CURSOR_DESTROY and state == GLUT_UP:
        primitive.scale(1.5)
    elif button == GLUT_CURSOR_HELP and state == GLUT_UP:
        primitive.scale(0.75)


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

    print("=QUALITY=")
    print(" Press + to increase subdivision count")
    print(" Press - to decrease subdivision count")
    print("=TRANSFORMATION=")
    print(" Left arrow to rotate around y axis (cw).")
    print(" Right arrow to rotate around y axis (ccw).")
    print(" Up arrow to rotate around x axis (cw).")
    print(" Down arrow to rotate around x axis (ccw).")
    print(" Scrool mouse wheel up to zoom in")
    print(" Scroll mouse wheel down to zoom out")
    print(" Right click to undo transformations")

    glutInit(argv[2:])

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)

    glutCreateWindow("IZTECH CENG487 - 10 2021 - 250201041")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyboardFunc)
    glutSpecialFunc(specialFunc)
    glutMouseFunc(mouseFunc)
    InitGL(640, 480)
    glutMainLoop()


if __name__ == "__main__":
    main()
