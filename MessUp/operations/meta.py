import weakref
import numpy as np
try:
    from .wrapper import Sequential
except Exception:
    from wrapper import Sequential
from itertools import zip_longest
from collections import ChainMap
import random
class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()
    
    def __call__(self, *args, **kwargs):
        # TODO: kwargs
        assert len(args) == 0
        # TODO: before perfect
        if False: # args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args, **kwargs)
            self.__cache[args] = obj
            return obj

class Operation(metaclass = Cached):
    def __init__(self, **kwargs):
        self._parameters = {}
        self._random_parameters = {}
        for parameter, value in kwargs.items():
            if parameter.startswith('r_'):
                self._random_parameters[parameter[2:]] = value
            else:
                self._parameters[parameter] = value
        # for name, value in ChainMap(dict(zip_longest(self._fields, args)), kwargs).items():
        #     setattr(self, name, value)

    def __str__(self):
        return '{} {} {}'.format(self.__class__.__name__, self._random_parameters, self._parameters)

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
        for parameter in self._fields:
            if parameter not in self.__dict__:
                self.__dict__['parameter'] = None
    def call(self, inputs, **kwargs):
        # parameters are image(np.ndarray)
        if isinstance(inputs, np.ndarray):
            self._instantiate_parameters()
            output = self.perform_on_image(inputs, **kwargs)
            # print(len(output))
            return output
        # parameters are list(multi image)
        elif isinstance(inputs, list):
            if 'sync' in kwargs and kwargs['sync']:
                pass
            
            self._instantiate_parameters()
            return self.perform_on_images(inputs)
        else:
        # parameters are another Operation or Wrapper
            return Sequential(self, inputs)
    
    def perform_on_images(self, imgs, sync = True):
        outputs = [self.perform_on_image(i) for i in imgs]
        return outputs

    def perform_on_image(self, img):
        raise NotImplementedError()

    def __call__(self, inputs, **kwargs):
        return self.call(inputs, **kwargs)


if __name__ == '__main__':
    # test cache
    op1 = Operation(test1 = 1, test2 = 2)
    op2 = Operation(test2 = 2, test1 = 1)
    op3 = Operation(test1 = 2, test2 = 2)
    print(op1 == op2, op1 == op3)
