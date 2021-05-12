from ObjectPools.ObjectPoolPolynomial import PolynomialPool
from ObjectPools.ObjectPoolMatrixM import MatrixPool
from ObjectPools.ObjectPoolVectorSum import VectorPool
from ObjectPools.Builder import PolynomialBuilder, MatrixBuilder, VectorBuilder
import threading


# test polynomial
def polynomial_build_threads():
    min_element_in_pool = 3
    max_pool_size = 10
    pool = PolynomialPool(min_element_in_pool, max_pool_size)
    amount = 7

    builder = PolynomialBuilder()
    builder.set_pool(pool)
    builder.set_amount(amount)
    builder.set_configuration([i for i in range(4)], 4)

    builder.get_result()


def threads_polynomial():
    threads = []
    for _ in range(5):
        t = threading.Thread(target=polynomial_build_threads)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def test_polynomial_roots(benchmark):
    benchmark.pedantic(threads_polynomial, iterations=5)


# test matrix
def matrix_build_threads():
    min_element_in_pool = 3
    max_pool_size = 10
    pool = MatrixPool(min_element_in_pool, max_pool_size)
    amount = 7

    builder = MatrixBuilder()
    builder.set_pool(pool)
    builder.set_amount(amount)
    builder.set_configuration([[1, 1], [2, 2]], [[3, 1], [0, 4]],
                              matrix_a_row=2, matrix_a_column=2, matrix_b_row=2, matrix_b_column=2)

    builder.get_result()


def threads_matrix():
    threads = []
    for _ in range(5):
        t = threading.Thread(target=matrix_build_threads)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def test_matrix_multiplication(benchmark):
    benchmark.pedantic(threads_matrix, iterations=5)


# test vector
def vector_build_threads():
    min_element_in_pool = 3
    max_pool_size = 10
    pool = VectorPool(min_element_in_pool, max_pool_size)
    amount = 7

    builder = VectorBuilder()
    builder.set_pool(pool)
    builder.set_amount(amount)
    builder.set_configuration([1, 1, 1, 1], [2, 2, 2, 2], 4, 4)

    builder.get_result()


def threads_vector():
    threads = []
    for _ in range(5):
        t = threading.Thread(target=vector_build_threads)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def test_vector_sum_threads(benchmark):
    benchmark.pedantic(threads_vector, iterations=5)
