from abc import ABC, abstractmethod
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class BaseApplication(ABC):
    def __init__(self,
                 title: str,
                 mode=GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH,
                 size=(640, 480),
                 pos=(0, 0),
                 argv=[]) -> None:
        self.title = title
        self.size = size
        self.mode = mode
        self.pos = pos
        self.argv = argv

    def init_gl(self):
        width, height = self.size

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)

    def start(self):
        glutInit(self.argv)

        glutInitDisplayMode(self.mode)
        glutInitWindowSize(*self.size)
        glutInitWindowPosition(*self.pos)

        glutCreateWindow(self.title)

        glutDisplayFunc(self.on_display)
        glutIdleFunc(self.on_idle)
        glutReshapeFunc(self.on_resize)
        glutKeyboardFunc(self.on_key_press)
        glutSpecialFunc(self.on_special_key_press)
        glutMouseFunc(self.on_mouse_click)
        glutPassiveMotionFunc(self.on_mouse_move)

        self.init_gl()
        glutMainLoop()

    def on_display(self):
        pass

    def on_idle(self):
        pass

    def on_resize(self, width, height):
        pass

    def on_key_press(self, key, x, y):
        pass

    def on_special_key_press(self, key, x, y):
        pass

    def on_mouse_click(self, button, state, x, y):
        pass

    def on_mouse_move(self, x, y):
        pass
