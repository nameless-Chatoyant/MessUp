try:
    from .meta import Operation
except Exception:
    from meta import Operation
import cv2
import numpy as np
import random

class Doodles_Crop_BonePoint(Operation):
    _fields = ['crop_px']
    def perform_on_image(self, img):
        h, w = img.shape[:2]
        crop_h, crop_w = self.crop_px
        if h < crop_h or w < crop_w:
            raise RuntimeError('Shape of cropping image must be larger than `crop_px`, ({}, {}) < ({}, {})'.format(h, w, *self.crop_px))
        if h - crop_h - 1 > 0:
            h_start = random.randint(0, h - crop_h - 1)
        else:
            h_start = 0
        if w - crop_w - 1 > 0:
            w_start = random.randint(0, w - crop_w - 1)
        else:
            w_start = 0
        if h - h_start - crop_h - 1 > 0:
            h_end = random.randint(h_start + crop_h, h - 1)
        else:
            h_end = h - 1
        if w - w_start - crop_w - 1 > 0:
            w_end = random.randint(w_start + crop_w, w - 1)
        else:
            w_end = w - 1

        res = img[h_start:h_end, w_start:w_end]
        
        return res, h_start, w_start

class Doodles_Crop(Operation):
    _fields = ['crop_px']
    def perform_on_images(self, imgs):
        def are_same_shape(shapes):
            shape = shapes[0]
            for i in shapes:
                if i != shape:
                    return False
            return True
        check_res = are_same_shape([i.shape[:2] for i in imgs])
        if not check_res:
            raise RuntimeError('not same shape')
        h, w = imgs[0].shape[:2]
        crop_h, crop_w = self.crop_px
        if h < crop_h or w < crop_w:
            raise RuntimeError('Shape of cropping image must be larger than `crop_px`, ({}, {}) < ({}, {})'.format(h, w, *self.crop_px))
        if h - crop_h - 1 > 0:
            h_start = random.randint(0, h - crop_h - 1)
        else:
            h_start = 0
        if w - crop_w - 1 > 0:
            w_start = random.randint(0, w - crop_w - 1)
        else:
            w_start = 0
        if h - h_start - crop_h - 1 > 0:
            h_end = random.randint(h_start + crop_h, h - 1)
        else:
            h_end = h - 1
        if w - w_start - crop_w - 1 > 0:
            w_end = random.randint(w_start + crop_w, w - 1)
        else:
            w_end = w - 1

        res = [i[h_start:h_end, w_start:w_end] for i in imgs]
        
        return res
    def perform_on_image(self, img):
        h, w = img.shape[:2]
        crop_h, crop_w = self.crop_px
        if h < crop_h or w < crop_w:
            raise RuntimeError('Shape of cropping image must be larger than `crop_px`, ({}, {}) < ({}, {})'.format(h, w, *self.crop_px))
        if h - crop_h - 1 > 0:
            h_start = random.randint(0, h - crop_h - 1)
        else:
            h_start = 0
        if w - crop_w - 1 > 0:
            w_start = random.randint(0, w - crop_w - 1)
        else:
            w_start = 0
        if h - h_start - crop_h - 1 > 0:
            h_end = random.randint(h_start + crop_h, h - 1)
        else:
            h_end = h - 1
        if w - w_start - crop_w - 1 > 0:
            w_end = random.randint(w_start + crop_w, w - 1)
        else:
            w_end = w - 1

        res = img[h_start:h_end, w_start:w_end]
        
        return res
if __name__ == '__main__':
    img1 = np.ones((64,32))
    img2 = np.zeros((64,32))
    res1, res2 = Doodles_Crop(crop_px = (30, 30))([img1, img2])
    print(res1.shape, res2.shape)
