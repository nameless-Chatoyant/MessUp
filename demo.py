from augmentor.operations import Distort

from PIL import Image
import cv2
import math
import random
import numpy as np
from scipy import misc


ds = Distort(1.0, 3, 3, 3)
# ds = ProjectOntoCylinder(1.0,3,4)

for i in range(1, 31):
    img = Image.open('a/{}.png'.format(i))
    # img = np.asarray(img)
    img = ds.perform_operation(img)
    img = np.asarray(img)
    misc.imsave('a/{}_after.png'.format(i), img)
