class Wrapper(object):
    def call(self, img):
        raise RuntimeError("Illegal call to a Wrapper instance.")
    def __call__(self,inputs):
        pass



class Sequential(Wrapper):
    def __init__(self, operations, random_order):
        # self.probability = probability
        self.random_order = random_order
        pass

    def __str__(self):
        return self.__class__.__name__

    

class Sometimes(Wrapper):
    pass

class OneOf(Wrapper):
    pass

class SomeOf(Wrapper):
    pass

"""
x = OneOf(

)(x)
"""