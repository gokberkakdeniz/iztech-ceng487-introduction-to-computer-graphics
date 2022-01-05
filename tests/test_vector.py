# CENG 487 Assignment7 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

import unittest
from lib.math import Vec3d
from math import pi, sqrt


class vec3dTest(unittest.TestCase):
    def setUp(self):
        self.point = Vec3d.point(1, 2, 3)
        self.point_one = Vec3d.point(1, 1, 1)
        self.vector = Vec3d.vector(1, 2, 3)
        self.vector_one = Vec3d.vector(1, 1, 1)
        self.vector_one_right = Vec3d.vector(1, 0, 0)
        self.vector_zero = Vec3d.vector(0, 0, 0)

    def test_equality(self):
        self.assertEqual(self.point, self.point)
        self.assertEqual(Vec3d.vector(1, 2, 3), Vec3d.vector(1, 2, 3))

    def test_clone(self):
        self.assertEqual(self.point, self.point.clone())

    def test_multiplication_by_number(self):
        expected = Vec3d(2, 2, 2, 2)
        self.assertEqual(self.point_one * 2, expected)
        self.assertEqual(2 * self.point_one, expected)

        expected = Vec3d(2, 4, 6, 2)
        self.assertEqual(self.point * 2, expected)
        self.assertEqual(2 * self.point, expected)

        expected = Vec3d(pi, pi, pi, pi)
        self.assertEqual(self.point_one * pi, expected)
        self.assertEqual(pi * self.point_one, expected)

        expected = Vec3d(pi, 2 * pi, 3 * pi, pi)
        self.assertEqual(self.point * pi, expected)
        self.assertEqual(pi * self.point, expected)

    def test_division_by_number(self):
        self.assertEqual(self.point_one / 2, Vec3d(1/2, 1/2, 1/2, 1/2))
        self.assertEqual(self.point / 2, Vec3d(1/2, 2/2, 3/2, 1/2))
        self.assertEqual(self.point_one / pi, Vec3d(1/pi, 1/pi, 1/pi, 1/pi))
        self.assertEqual(self.point / pi, Vec3d(1/pi, 2/pi, 3/pi, 1/pi))

    def test_vector_addition(self):
        self.assertEqual(self.vector + self.vector_one, Vec3d.vector(2, 3, 4))

    def test_point_addition(self):
        self.assertEqual(self.point + self.point_one, Vec3d(2, 3, 4, 2))

    def test_unary_minus(self):
        self.assertEqual(-self.point_one, Vec3d.point(-1, -1, -1))
        self.assertEqual(-self.vector_one, Vec3d.vector(-1, -1, -1))

    def test_unary_minus(self):
        self.assertEqual(+self.point_one, self.point_one)
        self.assertEqual(+self.vector_one, self.vector_one)

    def test_length(self):
        self.assertEqual(self.point_one.length(), 2)
        self.assertEqual(self.vector.length(), sqrt(14))

    def test_dot_product(self):
        self.assertEqual(self.vector.dot(self.point_one), 1+2+3+0)

    def test_cross_product(self):
        self.assertEqual(self.vector.cross(self.vector), self.vector_zero)
        self.assertEqual(
            self.vector.cross(self.vector_one),
            -self.vector_one.cross(self.vector)
        )

    def test_angle(self):
        self.assertEqual(self.vector.angle(self.vector), 0)
        self.assertAlmostEqual(
            Vec3d.vector(1, 0, 1).angle(Vec3d.vector(1, 0, 0)),
            pi/4
        )

    def test_project(self):

        self.assertEqual(
            Vec3d.vector(1, 1, 0).project(Vec3d.vector(1, 0, 0)),
            Vec3d.vector(1, 0, 0)
        )
        self.assertEqual(
            Vec3d.vector(3, 4, 0).project(Vec3d.vector(0, 2, 0)),
            Vec3d.vector(0, 4, 0)
        )
        self.assertAlmostEqual(
            Vec3d.vector(3, 4, 0).project(Vec3d.vector(-1, 0, 0)).length(),
            Vec3d.vector(3, 0, 0).length()
        )

    def test_normalize(self):
        self.assertEqual(Vec3d.vector(3, 4, 0).normalize(),
                         Vec3d.vector(3/5, 4/5, 0))

    def test_vec3d_multiply_by_nonnumber_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.point_one * self.point_one
            self.point_one * self.vector_one
            self.vector_one * self.point_one
            self.vector_one * self.vector_one
            self.vector_one * object()

    def test_vec3d_divided_by_nonnumber_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.point / self.point_one
            self.vector / self.vector_one
            self.vector / object()

    def test_number_divided_by_vec3d_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            1 / self.point
            1 / self.vector

    def test_getitem(self):
        self.assertEqual(self.vector[0], 1)
        self.assertEqual(self.vector[1], 2)
        self.assertEqual(self.vector[2], 3)
        self.assertEqual(self.vector[3], 0)

    def test_setitem(self):
        vec = self.vector_zero.clone()
        vec[0] = 1
        vec[1] = 2
        vec[2] = 3
        vec[3] = 1
        self.assertEqual(vec, self.point)


if __name__ == '__main__':
    unittest.main()
