import unittest
from lib.vector import vec3d
from math import pi


class vec3dTest(unittest.TestCase):
    def setUp(self):
        self.point = vec3d.point(1, 2, 3)
        self.point_one = vec3d.point(1, 1, 1)
        self.vector = vec3d.vector(1, 2, 3)
        self.vector_one = vec3d.vector(1, 1, 1)

    def test_multiplication_by_number(self):
        expected = vec3d.point(2, 2, 2)
        self.assertEqual(self.point_one * 2, expected)
        self.assertEqual(2 * self.point_one, expected)

        expected = vec3d.point(2, 4, 6)
        self.assertEqual(self.point * 2, expected)
        self.assertEqual(2 * self.point, expected)

        expected = vec3d.point(pi, pi, pi)
        self.assertEqual(self.point_one * pi, expected)
        self.assertEqual(pi * self.point_one, expected)

        expected = vec3d.point(pi, 2 * pi, 3 * pi)
        self.assertEqual(self.point * pi, expected)
        self.assertEqual(pi * self.point, expected)

    def test_division_by_number(self):
        self.assertEqual(self.point_one / 2, vec3d.point(1/2, 1/2, 1/2))
        self.assertEqual(self.point / 2, vec3d.point(1/2, 2/2, 3/2))
        self.assertEqual(self.point_one / pi, vec3d.point(1/pi, 1/pi, 1/pi))
        self.assertEqual(self.point / pi, vec3d.point(1/pi, 2/pi, 3/pi))

    def test_vector_addition(self):
        self.assertEqual(self.vector + self.vector_one, vec3d.vector(2, 3, 4))

    def test_point_addition(self):
        self.assertEqual(self.point + self.point_one, vec3d.point(2, 3, 4))

    def test_unary_minus(self):
        self.assertEqual(-self.point_one, vec3d.point(-1, -1, -1))
        self.assertEqual(-self.vector_one, vec3d.vector(-1, -1, -1))

    def test_unary_minus(self):
        self.assertEqual(+self.point_one, self.point_one)
        self.assertEqual(+self.vector_one, self.vector_one)

    def test_length(self):
        pass

    def test_dot_product(self):
        pass

    def test_cross_product(self):
        pass

    def test_angle(self):
        pass

    def test_project(self):
        pass

    def test_normalize(self):
        self.assertEqual(self.point_one.normalize(),
                         vec3d.point(1/2, 1/2, 1/2))
        self.assertEqual(vec3d.vector(3, 4, 0).normalize(),
                         vec3d.vector(3/5, 4/5, 0))

    def test_point_minus_vector_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.point - self.vector

    def test_vector_minus_point_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.vector - self.point

    def test_point_plus_vector_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.point + self.vector

    def test_vector_plus_point_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.vector + self.point

    def test_point_multiply_by_point_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.point_one * self.point_one

    def test_point_multiply_by_vector_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.point_one * self.vector_one

    def test_vector_multiply_by_point_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.vector_one * self.point_one

    def test_vector_multiply_by_vector_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.vector_one * self.vector_one

    def test_point_divided_by_point_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.point / self.point_one

    def test_vector_divided_by_vector_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.vector / self.vector_one

    def test_number_divided_by_point_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            1 / self.point

    def test_number_divided_by_vector_must_raise_type_error(self):
        with self.assertRaises(TypeError):
            1 / self.vector


if __name__ == '__main__':
    unittest.main()
