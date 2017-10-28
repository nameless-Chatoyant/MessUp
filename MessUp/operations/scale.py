try:
    from .meta import Operation
except Exception:
    from meta import Operation
import cv2
import numpy as np

class Resize(Operation):
    _fields = ['dsize', 'fx', 'fy']
    def perform_on_image(self, img):
        h, w = img.shape[:2]
        if self.dsize:
            d_h, d_w = self.dsize
            if d_h is not None and d_w is not None:
                res = cv2.resize(img, (d_w, d_h))
            elif d_h is None and d_w is not None:
                scale = w / d_w
                res = cv2.resize(img, None, fx=scale, fy=scale)
            elif d_h is not None and d_w is None:
                scale = h / d_h
                res = cv2.resize(img, None, fx=scale, fy=scale)
            else:
                print('?????')
        else:
            res = cv2.resize(img, None, fx = self.fx, fy = self.fy)
        return res
