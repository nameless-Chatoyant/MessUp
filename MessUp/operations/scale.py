try:
    from .meta import Operation
except Exception:
    from meta import Operation
import cv2
import numpy as np

class Resize(Operation):
    _fields = ['dsize', 'fx', 'fy', 'interpolation']
    def perform_on_image(self, img):
        h, w = img.shape[:2]
        if self.dsize:
            d_h, d_w = self.dsize
            if d_h is not None and d_w is not None:
                # print('before:', img.shape)
                if 'interpolation' in self.__dict__ and  self.interpolation == 'nearest':
                    res = cv2.resize(img, (d_w, d_h), interpolation=cv2.INTER_NEAREST)
                else:
                    res = cv2.resize(img, (d_w, d_h))
                # print('after:', img.shape)
            elif d_h is None and d_w is not None:
                scale = d_w/w
                if 'interpolation' in self.__dict__ and self.interpolation == 'nearest':
                    res = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
                else:
                    res = cv2.resize(img, None, fx=scale, fy=scale)
            elif d_h is not None and d_w is None:
                scale = d_h/h
                if 'interpolation' in self.__dict__ and self.interpolation == 'nearest':
                    res = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
                else:
                    res = cv2.resize(img, None, fx=scale, fy=scale)
            else:
                print('?????')
        else:
            res = cv2.resize(img, None, fx = self.fx, fy = self.fy)
        return res
