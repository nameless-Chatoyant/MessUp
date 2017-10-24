import weakref
import numpy as np

from .wrapper import Sequential
from itertools import zip_longest
from collections import ChainMap
import random
class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()
    
    def __call__(self, *args, **kwargs):
        # TODO: kwargs
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args, **kwargs)
            self.__cache[args] = obj
            return obj

class Operation(metaclass = Cached):
    _parameters = {}
    _random_parameters = {}
    def __init__(self, **kwargs):
        for parameter, value in kwargs.items():
            if parameter.startswith('r_'):
                self._random_parameters[parameter[2:]] = value
            else:
                self._parameters[parameter] = value
        # for name, value in ChainMap(dict(zip_longest(self._fields, args)), kwargs).items():
        #     setattr(self, name, value)
        print(self._parameters, self._random_parameters)

    def __str__(self):
        return '{} {}'.format(self.__class__.__name__, self.__dict__)

    def draw_sample(self):
        for i in self._fields:
            print(i, getattr(self, i))

    def _instantiate_parameters(self):
        for parameter, value in self._parameters.items():
            setattr(self, parameter, value)
        for parameter, value in self._random_parameters.items():
            if isinstance(value[0], float):
                setattr(self, parameter, random.uniform(value[0], value[1]))
            else:
                setattr(self, parameter, random.randint(value[0], value[1]))

    def call(self, inputs, **kwargs):
        if isinstance(inputs, np.ndarray):
            self._instantiate_parameters()
            output = self.perform_on_image(inputs, **kwargs)
            return output
        else:
            return Sequential(self, inputs)

    def perform_on_image(self, img):
        raise NotImplementedError()

    def __call__(self, inputs, **kwargs):
        return self.call(inputs, **kwargs)
