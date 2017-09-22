from .meta import Operation

import cv2
import numpy as np

class Dislocate(Operation):
    _fields = ['scale']
    def perform_on_image(self, img):
        def shift(m, n):
            if n > 0:
                return np.pad(m,((n,0)), mode='constant', constant_values=255)[:n]
            else:
                return np.pad(m,((0,-n)), mode='constant', constant_values=255)[-n:]
        h, w = img.shape[:2]
        mask = np.sin(np.arange(w) / self.scale) > 0
        for i in range(w):
            if mask[i]:
                img[:,i] = shift(img[:,i], -1)
        return img

class ProjectOntoCylinder(Operation):
    _fields = ['center', 'focal']
    def perform_on_image(self, img):
        # define mapping functions
        focal = self.focal
        center = self.center
        scale = focal
        mapX = lambda y, x: focal * np.tan(x/scale)
        mapY = lambda y, x: focal / np.cos(x/scale) * y/scale
        def makeMap(y, x):
            map_x = mapX(y - center[1], x - center[0]) + center[0]
            map_y = mapY(y - center[1], x - center[0]) + center[1]
            return np.dstack((map_x, map_y)).astype(np.int16)
        # create the LUTs for x and y coordinates
        map_xy = np.fromfunction(makeMap, img.shape[:2], dtype = np.int16)
        img_mapped = cv2.remap(img, map_xy, None, cv2.INTER_NEAREST)

        return img_mapped
