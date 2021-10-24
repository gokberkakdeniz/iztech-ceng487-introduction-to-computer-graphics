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


# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# A general OpenGL initialization function.  Sets all of the initial parameters.


# We call this right after our OpenGL window is created.
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

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)


def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    # Reset The Current Viewport And Perspective Transformation
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# The main drawing function.


def DrawGLScene():
    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()					# Reset The View

    # Move Left 1.5 units and into the screen 6.0 units.
    glTranslatef(-1.5, 0.0, -6.0)

    # Since we have smooth color mode on, this will be great for the Phish Heads :-).
    # Draw a triangle
    # glBegin(GL_POLYGON)                 # Start drawing a polygon
    # glColor3f(1.0, 0.0, 0.0)            # Red
    # glVertex3f(0.0, 1.0, 0.0)           # Top
    # glColor3f(0.0, 1.0, 0.0)            # Green
    # glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
    # glColor3f(0.0, 0.0, 1.0)            # Blue
    # glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
    # glEnd()                             # We are done with the polygon

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
    triangle.draw()

    # Move Right 3.0 units.
    glTranslatef(3.0, 0.0, 0.0)

    # Draw a square (quadrilateral)
    # glColor3f(0.3, 0.5, 1.0)            # Bluish shade
    # glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
    # glVertex3f(-1.0, 1.0, 0.0)          # Top Left
    # glVertex3f(1.0, 1.0, 0.0)           # Top Right
    # glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
    # glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
    # glEnd()                             # We are done with the polygon

    square = Shape(
        vertices=[
            Vec3d.point(-1.0, 1.0, 0.0),
            Vec3d.point(1.0, 1.0, 0.0),
            Vec3d.point(1.0, -1.0, 0.0),
            Vec3d.point(-1.0, -1.0, 0.0),
        ],
        color=(0.3, 0.5, 1.0)
    )
    square.transform(Mat3d.scaling_matrix(0.5, 0.5, 0.5))
    square.transform(Mat3d.rotation_z_matrix(pi/4))
    square.transform(Mat3d.rotation_z_matrix(-pi/4))
    square.transform(Mat3d.scaling_matrix(2, 2, 0))
    square.draw()

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)


def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        sys.exit()


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


# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")
main()
