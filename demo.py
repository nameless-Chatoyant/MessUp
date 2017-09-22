from MessUp.operations import *
from scipy import misc


img = misc.imread('a/1.png')
img = Dislocate(2)(img)
h, w = img.shape[:2]
img = ProjectOntoCylinder((w//2, h//2),200)(img)

aug = Dislocate(2)(ProjectOntoCylinder((w//2, h//2),200))
print(aug)
misc.imsave('output.png', img)