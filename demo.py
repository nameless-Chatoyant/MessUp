from MessUp.operations import *
from scipy import misc
import os

# icons = [os.path.join(dirpath, filename) for dirpath, dirname, filenames in os.walk('icons') for filename in filenames]
# for i in icons:
#     name = i.split('/')[-1]
#     img = misc.imread(i)
#     # Distort
#     # img = Distort(3,3,7)(img)
#     # Rotate
#     img = Rotate(r_degree = (-20, 20))(img)
#     # Resize
#     # img = Resize(None, (0.8, 1.2),(0.8, 1.2))(img)
    
#     misc.imsave('icons_out/'+name, img)
rotate = Rotate(r_degree = (-20, -20))
op = Distort(grid_w = 3, grid = 3, magnitude = 3)
op2 = op(rotate)
print(rotate)
print(op, op2)
img = misc.imread('test.png')
print(img.shape)
img = rotate(img)
print(img.shape)
misc.imsave('out.png', img)
