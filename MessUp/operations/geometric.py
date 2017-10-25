from .meta import Operation

from PIL import Image
import numpy as np


class Rotate(Operation):
    _fields = ['degree']
    def perform_on_image(self, img):
        img_pil = Image.fromarray(img)
        after = img_pil.rotate(self.degree)
        res = np.array(after)
        return res
