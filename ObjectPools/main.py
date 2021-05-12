from ObjectPools.ObjectPoolPolynomial import PolynomialPool
from ObjectPools.ObjectPoolMatrixM import MatrixPool
from ObjectPools.ObjectPoolVectorSum import VectorPool
from ObjectPools.Builder import PolynomialBuilder, MatrixBuilder, VectorBuilder


def test_polynomial_builder():
    min_element_in_pool = 3
    max_pool_size = 10
    pool = PolynomialPool(min_element_in_pool, max_pool_size)

    amount = 7

    builder = PolynomialBuilder()
    builder.set_pool(pool)
    builder.set_amount(amount)
    builder.set_configuration([i for i in range(4)], 4)

    results = builder.get_result()
    print(results)


def test_matrix_builder():
    min_element_in_pool = 3
    max_pool_size = 10
    pool = MatrixPool(min_element_in_pool, max_pool_size)
    amount = 7

    builder = MatrixBuilder()
    builder.set_pool(pool)
    builder.set_amount(amount)
    builder.set_configuration([[1, 1], [2, 2]], [[3, 1], [0, 4]],
                              matrix_a_row=2, matrix_a_column=2, matrix_b_row=2, matrix_b_column=2)

    results = builder.get_result()
    print(results)


def test_vector_builder():
    min_element_in_pool = 3
    max_pool_size = 10
    pool = VectorPool(min_element_in_pool, max_pool_size)
    amount = 7

    builder = VectorBuilder()
    builder.set_pool(pool)
    builder.set_amount(amount)
    builder.set_configuration([1, 1, 1, 1], [2, 2, 2, 2], 4, 4)

    results = builder.get_result()
    print(results)


if __name__ == "__main__":
    test_polynomial_builder()
    print('-----------------------------------------------------------------------------------------------------------')
    test_matrix_builder()
    print('-----------------------------------------------------------------------------------------------------------')
    test_vector_builder()
    print('-----------------------------------------------------------------------------------------------------------')

