class Pipeline():
    def __init__(self):
        self.operations = []
        pass
    
    def from_(self):
        """Define the input dataflow of augmentor.
        """
        pass
    def to_(self):
        """Define the output dataflow of augmentor.
        """
        pass

    def add(self, operation):
        pass
    def sequential(self, random_order = False):
        pass

    def status(self):
        pass


    def __execute(self, img):
        for operation in self.operations:
            r = round(random.uniform(0, 1), 1)
            if r <= operation.probability:
                img = operation.perform_operation(img)
        
        return img
    def sample(self, n):
        """Randomly sample n data from dataflow.
        """
        # self.__execute()
        pass
    
    def traverse(self, n_per = 1):
        """Traverse all data from dataflow, generate n_per augmented data from each raw data.
        """
        pass
