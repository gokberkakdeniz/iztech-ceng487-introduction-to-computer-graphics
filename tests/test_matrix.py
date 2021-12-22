# CENG 487 Assignment5 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

import unittest
from math import pi
from lib.math import Mat3d, Vec3d


class vec3dTest(unittest.TestCase):
    def setUp(self):
        self.zero = Mat3d(
            Vec3d(0, 0, 0, 0),
            Vec3d(0, 0, 0, 0),
            Vec3d(0, 0, 0, 0),
            Vec3d(0, 0, 0, 0),
        )
        self.identity = Mat3d(
            Vec3d(1, 0, 0, 0),
            Vec3d(0, 1, 0, 0),
            Vec3d(0, 0, 1, 0),
            Vec3d(0, 0, 0, 1),
        )
        self.matrix = Mat3d(
            Vec3d(1, 0, 0, 2),
            Vec3d(0, 1, 0, 3),
            Vec3d(0, 0, 1, 4),
            Vec3d(0, 0, 0, 1),
        )
        self.point = Vec3d.point(1, 2, 3)

    def test_equality(self):
        self.assertEqual(self.identity, self.identity)
        self.assertEqual(
            Mat3d(
                Vec3d(1, 0, 444, 2),
                Vec3d(-55, 1, 0.55, 3),
                Vec3d(0, 9, 1, 4),
                Vec3d(111, pi, 1/3, 1),
            ), Mat3d(
                Vec3d(1, 0, 444, 2),
                Vec3d(-55, 1, 0.55, 3),
                Vec3d(0, 9, 1, 4),
                Vec3d(111, pi, 1/3, 1),
            )
        )

    def test_clone(self):
        self.assertEqual(self.identity, self.identity.clone())

    def test_unary_minus(self):
        self.assertEqual(-(-self.identity), self.identity)

    def test_unary_plus(self):
        self.assertEqual(+self.identity, self.identity)

    def test_matrix_multiply_scalar(self):
        self.assertEqual(self.zero * 5, self.zero)
        self.assertEqual(0 * self.identity, self.zero)
        self.assertEqual(pi * self.zero, self.zero)
        self.assertEqual(
            3 * self.identity,
            Mat3d(
                Vec3d(3, 0, 0, 0),
                Vec3d(0, 3, 0, 0),
                Vec3d(0, 0, 3, 0),
                Vec3d(0, 0, 0, 3),
            )
        )

    def test_matrix_plus_matrix(self):
        self.assertEqual(self.zero + self.zero, self.zero)
        self.assertEqual(self.zero + self.matrix, self.matrix)

    def test_matrix_minus_matrix(self):
        self.assertEqual(self.zero - self.zero, self.zero)
        self.assertEqual(self.zero - self.matrix, -self.matrix)

    def test_matrix_multiply_matrix(self):
        self.assertEqual(self.identity @ self.matrix, self.matrix)
        self.assertEqual(self.matrix @ self.identity, self.matrix)
        self.assertEqual(self.matrix @ self.zero, self.zero)
        self.assertEqual(
            self.matrix @ self.identity @ self.identity,
            self.matrix
        )
        self.assertEqual(
            Mat3d(
                Vec3d(1, 2, 3, 4),
                Vec3d(5, 6, 7, 8),
                Vec3d(9, 10, 11, 12),
                Vec3d(13, 14, 15, 16),
            ) @ Mat3d(
                Vec3d(17, 18, 19, 20),
                Vec3d(21, 22, 23, 24),
                Vec3d(25, 26, 27, 28),
                Vec3d(29, 30, 31, 32),
            ),
            Mat3d(
                Vec3d(250, 260, 270, 280),
                Vec3d(618, 644, 670, 696),
                Vec3d(986, 1028, 1070, 1112),
                Vec3d(1354, 1412, 1470, 1528),
            )
        )

    def test_matrix_multiply_vector(self):
        self.assertEqual(
            self.identity @ self.point, self.point
        )
        self.assertEqual(
            Mat3d(
                Vec3d(1, 0, 0, 10),
                Vec3d(0, 1, 0, 11),
                Vec3d(0, 0, 1, 12),
                Vec3d(0, 0, 0, 1),
            ) @ self.point,
            self.point + Vec3d(10, 11, 12, 0)
        )


if __name__ == '__main__':
    unittest.main()
