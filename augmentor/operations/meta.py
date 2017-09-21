class Operation(object):
    def __init__(self):
        pass

    def __str__(self):
        return '{} {}'.format(self.__class__.__name__,self.__dict__)

    def call(self, inputs, **kwargs):
        raise RuntimeError("Illegal call to base class.")

    def __call__(self, inputs, **kwargs):
        output = self.call(inputs, **kwargs)
        return output
