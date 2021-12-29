# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from abc import ABC
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from signal import signal, SIGINT


class Event:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.button = -1
        self.state = -1
        self.alt = False
        self.ctrl = False
        self.shift = False


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
        self.event = Event()
        self.mouse_x = 0
        self.mouse_y = 0

    def init_gl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_FLAT)

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
        glutMotionFunc(self.on_mouse_drag)
        glutPassiveMotionFunc(self.on_mouse_move)

        self.init_gl()

        signal(SIGINT, lambda *_: glutLeaveMainLoop())

        glutMainLoop()

    def on_display(self):
        pass

    def on_idle(self):
        pass

    def on_resize(self, width, height):
        if height == 0:
            height = 1

        self.size = (width, height)

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)

    def on_key_press(self, key, x, y):
        if ord(key) == 27:
            glutLeaveMainLoop()

    def on_special_key_press(self, key, x, y):
        pass

    def on_mouse_click(self, button, state, x, y):
        self.event.x = x
        self.event.y = y
        self.event.state = state
        self.event.button = button

        m = glutGetModifiers()
        self.event.alt = m & GLUT_ACTIVE_ALT
        self.event.ctrl = m & GLUT_ACTIVE_CTRL
        self.event.shift = m & GLUT_ACTIVE_SHIFT

        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_drag(self, x, y):
        pass

    def on_mouse_move(self, x, y):
        pass
