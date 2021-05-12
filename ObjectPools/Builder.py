import numpy as np
import multiprocessing


class Builder:
    def __init__(self):
        self.amount = 0
        self.pool = None
        self.configuration = 0

    def reset(self):
        self.amount = 0
        self.pool = None

    def set_pool(self, pool):
        self.pool = pool

    def set_amount(self, number):
        self.amount = number

    def set_configuration(self, *args):
        self.configuration = args

    def f(self, _):
        reusable_object = self.pool.acquire()
        reusable_object.set_values(self.configuration)
        result = reusable_object.calculate()
        self.pool.release(reusable_object)
        return result

    def get_result(self):
        with multiprocessing.Pool() as pool:
            results = pool.map(self.f, range(self.amount))
        return results


class PolynomialBuilder(Builder):
    def __init__(self):
        super().__init__()
        self.amount = 0
        self.pool = None
        self.configuration_array = []
        self.size = 0

    def set_configuration(self, array, size):
        self.configuration_array = array
        self.size = size

    def f(self, _):
        reusable_object = self.pool.acquire()
        reusable_object.set_values(self.configuration_array, self.size)
        result = reusable_object.calculate()
        self.pool.release(reusable_object)
        return result


class MatrixBuilder(Builder):

    def __init__(self):
        super().__init__()
        self.amount = 0
        self.pool = None
        self.matrix_a_row = 0
        self.matrix_a_column = 0
        self.matrix_b_row = 0
        self.matrix_b_column = 0
        self.matrix_a = []
        self.matrix_b = []

    def set_configuration(self, matrix_a, matrix_b, matrix_a_row, matrix_a_column, matrix_b_row, matrix_b_column):
        self.matrix_a_row = matrix_a_row
        self.matrix_a_column = matrix_a_column
        self.matrix_b_row = matrix_b_row
        self.matrix_b_column = matrix_b_column
        self.matrix_a = matrix_a
        self.matrix_b = matrix_b

    def f(self, _):
        reusable_object = self.pool.acquire()
        reusable_object.set_values(self.matrix_a, self.matrix_b, self.matrix_a_row, self.matrix_a_column,
                                   self.matrix_b_row, self.matrix_b_column)
        result = reusable_object.calculate()
        self.pool.release(reusable_object)
        return result


class VectorBuilder(Builder):

    def __init__(self):
        super().__init__()
        self.amount = 0
        self.pool = None
        self.vector_a_size = 0
        self.vector_b_size = 0
        self.vector_a = []
        self.vector_b = []

    def set_configuration(self, vector_a, vector_b, vector_a_size, vector_b_size):
        self.vector_a_size = vector_a_size
        self.vector_b_size = vector_b_size
        self.vector_a = vector_a
        self.vector_b = vector_b

    def f(self, _):
        reusable_object = self.pool.acquire()
        reusable_object.set_values(self.vector_a, self.vector_b, self.vector_a_size, self.vector_b_size)
        result = reusable_object.calculate()
        self.pool.release(reusable_object)
        return result


class Director:
    def __init__(self, builder):
        self.builder = builder

    def construct(self):
        self.builder.reset()
        self.builder.set_prototype()
        self.builder.set_pool()
        self.builder.number_of_object(5)
        self.builder.configuration_of_object(list(np.random.randint(low=3, high=8, size=10)))

    def get_result(self):
        return self.builder.get_result()


def main():
    pass


main()
