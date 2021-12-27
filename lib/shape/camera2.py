
# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from OpenGL.GLU import projection
import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
from lib.math.vector import Vec3d

from lib.shape.shader import Resource
from ..math import Mat3d


class Camera2(Resource):
    def __init__(self):
        super().__init__()
        self.eye = Vec3d.point(0.0, 0.0, 0.0)
        self.center = Vec3d.point(0.0, 0.0, 0.0)
        self.up = Vec3d.vector(0.0, 0.0, 0.0)

        self.fov = 45
        self.near = 0.1
        self.far = 100
        self.aspect = 1
        self.cameraX = Vec3d.vector(0.0, 0.0, 0.0)
        self.cameraY = Vec3d.vector(0.0, 0.0, 0.0)
        self.cameraZ = Vec3d.vector(0.0, 0.0, 0.0)

        self.createView(Vec3d.point(0.0, 0.0, 6.0),
                        Vec3d.point(0.0, 0.0, 0.0),
                        Vec3d.vector(0.0, 1.0, 0.0))

        self.model_matrix = Mat3d.identity()

    def createView(self, eyePoint, centerPoint, upVector):
        self.eye = eyePoint
        self.orgEye = eyePoint

        self.center = centerPoint
        self.orgCenter = centerPoint

        self.up = upVector
        self.orgUp = upVector

        self.__compute_camera_space()

    def setFov(self, f):
        self.fov = f

    def getFov(self):
        return self.fov

    def setNear(self, n):
        self.near = n

    def getNear(self):
        return self.near

    def setFar(self, f):
        self.far = f

    def getFar(self):
        return self.far

    def getEyePoint(self):
        return self.eye

    def getCenterPoint(self):
        return self.center

    def getUpVector(self):
        return self.up

    def setMouseMode(self, mode):
        self.mouseMode = mode

    def getMouseMode(self):
        return self.mouseMode

    def camDistance(self):
        view = self.eye - self.center
        return view.length()

    def preDolly(self, x, y, z):
        unCam = self.__unrotate_camera()
        traCam = Mat3d.translation_matrix(x, y, z)
        toCam = self.__rotate_camera()
        return unCam @ traCam @ toCam

    def dolly(self, x, y, z):
        tx = self.preDolly(x, y, z)
        self.center = tx @ self.center
        self.eye = tx @ self.eye

    def zoom(self, z):
        tx = self.preDolly(0, 0, z)
        self.center = tx @ self.center
        self.eye = tx @ self.eye

    def dollyCamera(self, x, y, z):
        preViewVec = self.center - self.eye
        preViewVec = preViewVec.normalize()

        tx = self.preDolly(x, y, z)
        self.eye = tx @ self.eye

        postViewVec = self.center - self.eye
        postViewVec = postViewVec.normalize()

        preViewVecYZ = Vec3d.vector(0, preViewVec.y, preViewVec.z)
        preViewVecXZ = Vec3d.vector(preViewVec.x, 0, preViewVec.z)
        postViewVecYZ = Vec3d.vector(0, postViewVec.y, postViewVec.z)
        postViewVecXZ = Vec3d.vector(postViewVec.x, 0, postViewVec.z)

        try:
            angleX = postViewVecYZ.angle(preViewVecYZ)
        except ValueError:
            angleX = 0
        try:
            angleY = postViewVecXZ.angle(preViewVecXZ)
        except ValueError:
            angleY = 0

        rot1 = Mat3d.rotation_x_matrix(-angleX)
        rot2 = Mat3d.rotation_y_matrix(-angleY)
        tmp1 = rot1 @ rot2
        self.up = tmp1 @ self.up
        self.__compute_camera_space()

    def dollyCenter(self, x, y, z):
        tx = self.preDolly(x, y, z)
        self.center = tx @ self.center
        self.__compute_camera_space()

    def pan(self, d):
        moveBack = Mat3d.translation_matrix(self.eye.x, self.eye.y, self.eye.z)
        rot = self.__rotate_camera_y(d)
        move = Mat3d.translation_matrix(-self.eye.x, -self.eye.y, -self.eye.z)

        tmp1 = moveBack @ rot @ move

        self.center = tmp1 @ self.center
        self.up = tmp1 @ self.up

        self.__compute_camera_space()

    def tilt(self, d):
        moveBack = Mat3d.translation_matrix(self.eye.x, self.eye.y, self.eye.z)
        rot = self.__rotate_camera_x(d)
        move = Mat3d.translation_matrix(-self.eye.x, -self.eye.y, -self.eye.z)

        tmp1 = moveBack @ rot @ move

        self.center = tmp1 @ self.center
        self.up = tmp1 @ self.up

        self.__compute_camera_space()

    def roll(self, d):
        moveBack = Mat3d.translation_matrix(self.eye.x, self.eye.y, self.eye.z)
        rot = self.__rotate_camera_z(d)
        move = Mat3d.translation_matrix(-self.eye.x, -self.eye.y, -self.eye.z)

        tmp1 = moveBack @ rot @ move

        self.center = tmp1 @ self.center
        self.up = tmp1 @ self.up

        self.__compute_camera_space()

    def yaw(self, d):
        moveBack = Mat3d.translation_matrix(self.center.x, self.center.y, self.center.z)
        rot = self.__rotate_camera_y(d)
        move = Mat3d.translation_matrix(-self.center.x, -self.center.y, -self.center.z)

        tmp1 = moveBack @ rot @ move

        self.eye = tmp1 @ self.eye
        self.up = tmp1 @ self.up

        self.__compute_camera_space()

    def pitch(self, d):
        moveBack = Mat3d.translation_matrix(self.center.x, self.center.y, self.center.z)
        rot = self.__rotate_camera_x(d)
        move = Mat3d.translation_matrix(-self.center.x, -self.center.y, -self.center.z)

        tmp1 = moveBack @ rot @ move

        self.eye = tmp1 @ self.eye
        self.up = tmp1 @ self.up

        self.__compute_camera_space()

    def reset(self):
        self.eye = self.orgEye
        self.center = self.orgCenter
        self.up = self.orgUp
        self.model_matrix = Mat3d.identity()

        self.__compute_camera_space()

    def get_projection_matrix(self):
        f = np.reciprocal(np.tan(np.divide(np.deg2rad(self.fov), 2.0)))

        base = self.near - self.far
        term_0_0 = np.divide(f, self.aspect)
        term_2_2 = np.divide(self.far + self.near, base)
        term_2_3 = np.divide(np.multiply(np.multiply(2, self.near), self.far), base)

        return Mat3d(Vec3d(term_0_0, 0.0, 0.0, 0.0),
                     Vec3d(0.0, f, 0.0, 0.0),
                     Vec3d(0.0, 0.0, term_2_2, term_2_3),
                     Vec3d(0.0, 0.0, -1, 0.0))

    def get_view_matrix(self):
        R = Mat3d(self.cameraX,
                  self.cameraY,
                  -self.cameraZ,
                  Vec3d(0.0, 0.0, 0.0, 1.0))
        T = Mat3d.translation_matrix(-self.eye.x, -self.eye.y, -self.eye.z)

        return T @ R

    def get_model_matrix(self):
        return self.model_matrix

    def rotate_model(self, x: float, y: float, z: float):
        self.model_matrix @= Mat3d.rotation_matrix(x, y, z)

    def translate_model(self, x: float, y: float, z: float):
        self.model_matrix @= Mat3d.translation_matrix(x, y, z)

    def scale_model(self, x: float, y: float, z: float):
        self.model_matrix @= Mat3d.scaling_matrix(x, y, z)

    def load(self):
        model = self.get_model_matrix()
        view = self.get_view_matrix()
        projection = self.get_projection_matrix()

        if self.program is None:
            matrix = (projection @ view @ model).to_array()
            glLoadMatrixf(matrix)
        else:
            glUseProgram(self.program.id)

            modelLocation = glGetUniformLocation(self.program.id, "model")
            glUniformMatrix4fv(modelLocation, 1, GL_FALSE, model.to_array())

            viewLocation = glGetUniformLocation(self.program.id, "view")
            glUniformMatrix4fv(viewLocation, 1, GL_FALSE, view.to_array())

            projectionLocation = glGetUniformLocation(self.program.id, "projection")
            glUniformMatrix4fv(projectionLocation, 1, GL_FALSE, projection.to_array())

            cameraPosLocation = glGetUniformLocation(self.program.id, "cameraPos")
            glUniform4f(cameraPosLocation, *self.eye.to_list())

            glUseProgram(0)

    def __rotate_camera(self):

        return Mat3d(Vec3d(self.cameraX.x, self.cameraY.x, self.cameraZ.x, 0.0),
                     Vec3d(self.cameraX.y, self.cameraY.y, self.cameraZ.y, 0.0),
                     Vec3d(self.cameraX.z, self.cameraY.z, self.cameraZ.z, 0.0),
                     Vec3d(0.0,  0.0,  0.0, 1.0))

    def __unrotate_camera(self):
        return Mat3d(Vec3d(self.cameraX.x, self.cameraX.y, self.cameraX.z, 0.0),
                     Vec3d(self.cameraY.x, self.cameraY.y, self.cameraY.z, 0.0),
                     Vec3d(self.cameraZ.x, self.cameraZ.y, self.cameraZ.z, 0.0),
                     Vec3d(0.0, 0.0, 0.0, 1.0))

    def __rotate_camera_x(self, a):
        unCam = self.__unrotate_camera()
        rotCam = Mat3d.rotation_x_matrix(a)
        toCam = self.__rotate_camera()

        return unCam @ rotCam @ toCam

    def __rotate_camera_y(self, a):
        unCam = self.__unrotate_camera()
        rotCam = Mat3d.rotation_y_matrix(a)
        toCam = self.__rotate_camera()

        return unCam @ rotCam @ toCam

    def __rotate_camera_z(self, a):
        unCam = self.__unrotate_camera()
        rotCam = Mat3d.rotation_z_matrix(a)
        toCam = self.__rotate_camera()

        return unCam @ rotCam @ toCam

    def __compute_camera_space(self):
        self.cameraZ = (self.center - self.eye).normalize()
        self.cameraX = self.cameraZ.cross(self.up).normalize()
        self.cameraY = self.cameraX.cross(self.cameraZ)
