# CENG 487 Assignment1 by
# Gokberk Akdeniz
# StudentId:250201041
# 10 2021

from math import pi
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from lib.matrix import Mat3d
from lib.shape import Shape
from lib.vector import Vec3d
import sys
import time

# Number of the glut window.
window = 0
fps = 60


def InitGL(Width, Height):
    # This Will Clear The Background Color To Black
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    # Reset The Current Viewport And Perspective Transformation
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


triangle = Shape(
    vertices=[
        Vec3d.point(0.0, 1.0, 0.0),
        Vec3d.point(1.0, -1.0, 0.0),
        Vec3d.point(-1.0, -1.0, 0.0)
    ],
    color=[
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0)
    ]
)
triangle_rotation_vertice_index = 0
triangle.transform(
    Mat3d.scaling_matrix(0.6, 0.6, 0.6)
)
triangle.transform(
    Mat3d.translation_matrix(
        *(-triangle[triangle_rotation_vertice_index])[:-1]
    )
)

square = Shape(
    vertices=[
        Vec3d.point(-1.0, 1.0, 0.0),
        Vec3d.point(1.0, 1.0, 0.0),
        Vec3d.point(1.0, -1.0, 0.0),
        Vec3d.point(-1.0, -1.0, 0.0),
    ],
    color=(0.3, 0.5, 1.0)
)
square_rotation_vertice_index = 2
square.transform(
    Mat3d.scaling_matrix(0.6, 0.6, 0.6)
)
square.transform(
    Mat3d.translation_matrix(*(-square[square_rotation_vertice_index])[:-1])
)


def DrawGLScene():
    global angle, square, triangle

    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()					# Reset The View

    # Move Left 1.5 units and into the screen 6.0 units.
    glTranslatef(-1.5, 0.0, -6.0)

    triangle.transform(Mat3d.rotation_x_matrix(pi/120))
    triangle.transform(Mat3d.rotation_y_matrix(pi/120))
    triangle.transform(Mat3d.rotation_z_matrix(pi/60))
    triangle.draw()

    # Move Right 3.0 units.
    glTranslatef(3.0, 0.0, 0.0)

    square.transform(Mat3d.rotation_x_matrix(pi/120))
    square.transform(Mat3d.rotation_y_matrix(pi/120))
    square.transform(Mat3d.rotation_z_matrix(pi/60))
    square.draw()

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

    time.sleep(1/fps)


def keyPressed(key, x, y):
    global fps

    if ord(key) == 27:
        glutLeaveMainLoop()
        return
    elif key == b'+':
        fps = fps if fps > 300 else fps + 16
    elif key == b'-':
        fps = fps if fps < 16 else fps - 15
    elif key == b'0':
        fps = 60
    else:
        T = None
        if key == b'/':
            T = Mat3d.scaling_matrix(0.5, 0.5, 0.5)
        elif key == b'*':
            T = Mat3d.scaling_matrix(2, 2, 2)
        else:
            return

        triangle.transform(T)
        square.transform(T)


def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    # Alpha components supported
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(640, 480)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("CENG487 Template")

    # Display Func
    glutDisplayFunc(DrawGLScene)

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()


print("Hit ESC key to quit.")
print("Hit + to increase fps.")
print("Hit - to decrease fps.")
print("Hit 0 to reset fps.")
print("Hit * to scale up.")
print("Hit / to scale down.")
main()
