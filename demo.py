from MessUp.operations import *
from scipy import misc


img = misc.imread('test.png')
img = Resize((30, None))(img)
img = Dislocate(2)(img)
h, w = img.shape[:2]
img = ProjectOntoCylinder((w // 2, h // 2), 500)(img)
mask = img == 255
each_column = mask.all(0)
x_start = 0
x_end = 0
for i in range(w):
    if not each_column[i]:
        x_start = i
        break
for i in range(1,w):
    if not each_column[-i]:
        x_end = w - i + 1
        break
img = img[:,x_start:x_end]
misc.imsave('output.png', img)