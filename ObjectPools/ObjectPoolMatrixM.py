import multiprocessing
import numpy as np
from ObjectPools.Prototype import Prototype
from copy import deepcopy


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MatrixPool(metaclass=SingletonMeta):
    def __init__(self, min_element, max_size):
        self.prototype = MatrixObject()
        self.min_element = min_element
        self.max_size = max_size
        self.size = self.min_element

        m = multiprocessing.Manager()
        queue_initial = m.Queue()
        for _ in range(self.min_element):
            queue_initial.put(self.prototype.clone())
        self.available = queue_initial

    def acquire(self):
        if self.available.empty():
            if self.size == self.max_size:
                raise Exception('You cannot create more objects.')
            self.available.put(self.prototype.clone())
            self.size += 1

        result = self.available.get()
        return result

    def release(self, reusable):
        reusable.reset()
        self.available.put(reusable)

    def get_pool_size(self):
        return self.available.qsize()


class MatrixObject(Prototype):

    def __init__(self):
        self.matrix_a = np.zeros((1000, 1000))
        self.matrix_b = np.zeros((1000, 1000))
        self.matrix_a_row = self.matrix_a_column = self.matrix_b_row = self.matrix_b_column = 0
        self.result = 0

    def reset(self):
        self.matrix_a[:] = self.matrix_b[:] = 0
        self.matrix_a_row = self.matrix_a_column = self.matrix_b_row = self.matrix_b_column = 0
        self.result = 0

    def set_values(self, matrix_a, matrix_b, matrix_a_row, matrix_a_column, matrix_b_row, matrix_b_column):
        self.matrix_a_row = matrix_a_row
        self.matrix_a_column = matrix_a_column
        self.matrix_b_row = matrix_b_row
        self.matrix_b_column = matrix_b_column
        self.matrix_a[:self.matrix_a_row, :self.matrix_a_column] = matrix_a
        self.matrix_b[:self.matrix_b_row, :self.matrix_b_column] = matrix_b

    def get_values(self):
        return self.matrix_a[:self.matrix_a_row, :self.matrix_a_column], \
               self.matrix_b[:self.matrix_b_row, :self.matrix_b_column]

    def calculate(self):
        self.result = np.dot(self.matrix_a[:self.matrix_a_row, :self.matrix_a_column],
                             self.matrix_b[:self.matrix_b_row, :self.matrix_b_column])
        return self.result

    def get_result(self):
        return self.result

    def clone(self):
        return deepcopy(self)


def main():
    min_element_in_pool = 1
    max_pool_size = 10
    reusable_pool = MatrixPool(min_element_in_pool, max_pool_size)

    reusable_one = reusable_pool.acquire()
    reusable_two = reusable_pool.acquire()

    reusable_one.set_values([[1, 0, 1, 2, 3, 5], [0, 13, 2, 4, 5, 7], [2, 3, 4, 33, 5, 6], [6, 7, 8, -4, -2, -1],
                             [-1, -2, -33, -4, 5, 6], [3, 55, 21, 12, -9, -6]],
                            [[1, 111, 13, 2, 31, 5], [-110, 13, -2, 34, 5, 17], [-2, 31, 4, 3, 45, -6],
                             [6, 7, 8, -4, -2, -1], [-1, -2, 3, 4, 5, 60], [3, 55, 21, 12, 0, -6]],
                            matrix_a_row=6, matrix_a_column=6, matrix_b_row=6, matrix_b_column=6)

    reusable_two.set_values([[1, 1], [2, 2]], [[3, 1], [0, 4]],
                            matrix_a_row=2, matrix_a_column=2, matrix_b_row=2, matrix_b_column=2)

    print('ObjectOneResult = \n', reusable_one.calculate())
    print('ObjectTwoResult = \n', reusable_two.calculate())

    reusable_pool.release(reusable_one)
    reusable_pool.release(reusable_two)

    reusable_one = None
    reusable_two = None

    print('Release objects.')


if __name__ == "__main__":
    main()
