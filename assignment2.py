# CENG 487 Assignment1 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from math import atan, pi
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

from lib.shape import Torus, Box, Cylinder, Sphere

primitive = Sphere()
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


def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6.0)

    primitive.draw_border()
    primitive.draw()

    glutSwapBuffers()


def keyboardFunc(key, x, y):
    global primitive

    if ord(key) == 27:
        glutLeaveMainLoop()
    elif key == b'1':
        primitive = Sphere()
    elif key == b'2':
        primitive = Box()
    elif key == b'3':
        primitive = Cylinder()
    elif key == b'4':
        primitive = Torus()
    elif key == b'+':
        primitive.increase_subdivisions()
    elif key == b'-':
        primitive.decrease_subdivisions()


def mouseFunc(button, state, x, y):
    global mouse_x, mouse_y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:
            factor = (((mouse_y-y)**2 + (mouse_x-x)**2) /
                      (640**2 + 480**2))**0.5
            drag_angle = pi/2 if x == mouse_x else atan(
                (y-mouse_y)/((x-mouse_x)))
            primitive.rotate(factor*drag_angle*pi/2,
                             factor*drag_angle*pi/2,
                             factor*drag_angle*pi/2)
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
    InitGL(640, 480)
    glutMainLoop()


print("=OBJECTS=")
print(" Press 1 to show sphere")
print(" Press 2 to show box")
print(" Press 3 to show cylinder")
print(" Press 4 to show torus")
print("=QUALITY=")
print(" Press + to increase subdivision count")
print(" Press - to decrease subdivision count")
print("=TRANSFORMATION=")
print(" Scrool mouse wheel up to zoom in")
print(" Scroll mouse wheel down to zoom out")
print(" Drag and drop to rotate")
print(" Right click to undo transformations")

main()
