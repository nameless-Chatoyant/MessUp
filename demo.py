from MessUp.operations import *
from scipy import misc


img = misc.imread('test.png')
img = Resize((30, None))(img)
img = Dislocate(2)(img)
h, w = img.shape[:2]
img = ProjectOntoCylinder((w//2, h//2),500)(img)
misc.imsave('output.png', img)