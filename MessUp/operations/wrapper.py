# from .meta import Cached
import weakref
class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()
    
    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj


class Wrapper(metaclass = Cached):
    # _operations = []
    def __init__(self, *args, **kwargs):
        self.operations = args
    def call(self, img):
        raise RuntimeError("Illegal call to a Wrapper instance.")
    def __call__(self,inputs):
        pass
    def __str__(self):
        txt = self.__class__.__name__ + '\n' + '\n'.join(str(i) for i in self.operations)
        return txt



class Sequential(Wrapper):
    _f = {'random_order': False}
    

    

class Sometimes(Wrapper):
    pass

class OneOf(Wrapper):
    pass

class SomeOf(Wrapper):
    pass

class WithChannels(Wrapper):
    pass

"""

pair = Wrap()
x = OneOf(

)(x)
Distort()
"""