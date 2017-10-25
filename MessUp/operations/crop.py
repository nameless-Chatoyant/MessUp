from .meta import Operation

import cv2
import numpy as np
import random

class Crop(Operation):
    _fields = ['crop_px', 'crop_percent', 'center', 'keepsize']
    def perform_on_image(self, img):
        h, w = img.shape[:2]
        if h < self.crop_px or w < self.crop_px:
            raise RuntimeError('Shape of cropping image must be larger than `crop_px`, ({}, {}) < ({}, {})'.format(h, w, *self.crop_px))
        crop_h, crop_w = self.crop_px

        h_start = random.randint(0, h - crop_h - 1)
        w_start = random.randint(0, w - crop_w - 1)        

        res = img[h_start:h_start + crop_h, w_start:w_start + crop_w]
        
        return res
        
