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


class VectorPool(metaclass=SingletonMeta):
    def __init__(self, min_element, max_size):
        self.prototype = VectorObject()
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


class VectorObject(Prototype):

    def __init__(self):
        self.vector_a = np.zeros(1000)
        self.vector_b = np.zeros(1000)
        self.vector_a_size = self.vector_b_size = 0
        self.result = 0

    def reset(self):
        self.vector_a[:] = self.vector_b[:] = 0
        self.vector_a_size = self.vector_b_size = 0
        self.result = 0

    def set_values(self, vector_a, vector_b, vector_a_size, vector_b_size):
        self.vector_a_size = vector_a_size
        self.vector_b_size = vector_b_size
        self.vector_a[:self.vector_a_size] = vector_a
        self.vector_b[:self.vector_b_size] = vector_b

    def get_values(self):
        return self.vector_a[:self.vector_a_size], self.vector_b[:self.vector_b_size]

    def calculate(self):
        self.result = np.add(self.vector_a[:self.vector_a_size], self.vector_b[:self.vector_b_size])
        return self.result

    def get_result(self):
        return self.result

    def clone(self):
        return deepcopy(self)


def main():
    min_element_in_pool = 1
    max_pool_size = 10
    reusable_pool = VectorPool(min_element_in_pool, max_pool_size)

    reusable_one = reusable_pool.acquire()
    reusable_two = reusable_pool.acquire()

    reusable_one.set_values([1, 1, 1, 1], [2, 2, 2, 2], 4, 4)

    reusable_two.set_values([1, 1, 1, 1, -2, -4, -7, 8, 3, 5],
                            [1, 1, 1, 5, 4, -6, 7, 3, 12, 3], 10, 10)

    print('ObjectOneResult = ', reusable_one.calculate())
    print('ObjectTwoResult =', reusable_two.calculate())

    reusable_pool.release(reusable_one)
    reusable_pool.release(reusable_two)

    reusable_one = None
    reusable_two = None

    print('Release objects.')


if __name__ == "__main__":
    main()
