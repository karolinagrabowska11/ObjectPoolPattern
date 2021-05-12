import unittest
from ObjectPools.ObjectPoolPolynomial import PolynomialObject, PolynomialPool
from ObjectPools.ObjectPoolMatrixM import MatrixObject, MatrixPool
from ObjectPools.ObjectPoolVectorSum import VectorObject, VectorPool
from ObjectPools.Builder import PolynomialBuilder


class MyTestCase(unittest.TestCase):

    # operation testing
    def test_polynomial_roots(self):
        object_polynomial = PolynomialObject()
        object_polynomial.set_values([4, -1], 2)
        result = object_polynomial.calculate()
        self.assertEqual([0.25], result)

    def test_matrix_multiplication(self):
        object_matrix = MatrixObject()
        object_matrix.set_values([[1, 1], [2, 2]], [[3, 1], [0, 4]],
                                 matrix_a_row=2, matrix_a_column=2, matrix_b_row=2, matrix_b_column=2)
        result = object_matrix.calculate()
        self.assertEqual([[3., 5.], [6., 10.]], result.tolist())

    def test_vector_sum(self):
        object_vector = VectorObject()
        object_vector.set_values([1, 1, 1, 1], [2, 2, 2, 2], 4, 4)
        result = object_vector.calculate()
        self.assertEqual([3., 3., 3., 3.], result.tolist())

    # copy testing
    def test_copy(self):
        prototype = PolynomialObject()
        clone_object = prototype.clone()
        self.assertNotEqual(prototype, clone_object)

    # creating pool with min amount of object testing
    def test_min_object_pool(self):
        min_element_in_pool = 3
        max_pool_size = 10
        pool = MatrixPool(min_element_in_pool, max_pool_size)
        self.assertEqual(3, pool.get_pool_size())

    # testing error after acquiring too many objects from pool
    def test_max_object_pool(self):
        with self.assertRaises(Exception) as context:
            min_element_in_pool = 0
            max_pool_size = 5
            pool = PolynomialPool(min_element_in_pool, max_pool_size)
            for _ in range(max_pool_size+2):
                pool.acquire()

        self.assertTrue('You cannot create more objects.' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
