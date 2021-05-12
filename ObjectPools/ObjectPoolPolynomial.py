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


class PolynomialPool(metaclass=SingletonMeta):
    def __init__(self, min_element, max_size):
        self.prototype = PolynomialObject()
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


class PolynomialObject(Prototype):

    def __init__(self):
        self.coefficients_array = np.zeros(1000)
        self.array_size = 0
        self.result = 0

    def reset(self):
        self.coefficients_array[:] = 0
        self.array_size = 0
        self.result = 0

    def set_values(self, array, size):
        self.array_size = size
        self.coefficients_array[:self.array_size] = array

    def get_values(self):
        return self.coefficients_array[:self.array_size]

    def calculate(self):
        self.result = np.roots(self.coefficients_array[:self.array_size])
        return self.result

    def get_result(self):
        return self.result

    def clone(self):
        return deepcopy(self)


def main():
    min_element_in_pool = 3
    max_pool_size = 5
    reusable_pool = PolynomialPool(min_element_in_pool, max_pool_size)
    print('Number of objects in pool after initialization: ', reusable_pool.get_pool_size())

    reusable_one = reusable_pool.acquire()
    reusable_two = reusable_pool.acquire()

    array_size = 10
    reusable_one.set_values([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], array_size)
    reusable_two.set_values([1, 2, 3, 0], 4)

    print('Number of objects in pool: ', reusable_pool.get_pool_size())

    print('ObjectOneResult:', reusable_one.calculate())
    print('ObjectResult:', reusable_two.calculate())

    reusable_pool.release(reusable_one)
    reusable_pool.release(reusable_two)

    reusable_one = None
    reusable_two = None

    print('Release objects.')


if __name__ == "__main__":
    main()
