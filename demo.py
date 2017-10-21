from MessUp.operations import *
from scipy import misc
import os

icons = [os.path.join(dirpath, filename) for dirpath, dirname, filenames in os.walk('icons') for filename in filenames]
for i in icons:
    name = i.split('/')[-1]
    img = misc.imread(i)
    # Distort
    img = Distort(3,3,7)(img)
    # Rotate
    img = Rotate((-20, 20))(img)
    # Resize
    img = Resize(None, (0.8, 1.2),(0.8, 1.2))(img)
    
    misc.imsave('icons_out/'+name, img)
