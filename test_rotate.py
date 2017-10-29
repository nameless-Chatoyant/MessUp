from MessUp.operations import *
from scipy import misc

img = misc.imread('test.png')
# print(rotate_default, rotate_crop_valid, rotate_expand, sep = '\n')

res = Affine(degree = 20, direction = 'x')(img)
print(res.shape)
misc.imsave('output_expand.png', res)