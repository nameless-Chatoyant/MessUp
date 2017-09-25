import weakref
import numpy as np

from .wrapper import Sequential
from itertools import zip_longest

class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()
    
    def __call__(self, *args, **kwargs):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj

class Operation(metaclass = Cached):
    _fields = []
    def __init__(self, *args, **kwargs):
        # if len(args) != len(self._fields):
        #     raise TypeError('Expected {} arguments'.format(len(self._fields)))
        for name, value in zip_longest(self._fields, args):
            setattr(self, name, value)

    def __str__(self):
        return '{} {}'.format(self.__class__.__name__, self.__dict__)

    def draw_sample(self):
        for i in self._fields:
            print(i, getattr(self, i))

    def call(self, inputs, **kwargs):
        if isinstance(inputs, np.ndarray):
            output = self.perform_on_image(inputs, **kwargs)
            return output
        else:
            return Sequential(self, inputs)

    def perform_on_image(self, img):
        raise NotImplementedError()

    def __call__(self, inputs, **kwargs):
        return self.call(inputs, **kwargs)