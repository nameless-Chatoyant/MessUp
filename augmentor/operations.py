from PIL import Image
import cv2
import math
import random
import numpy as np
from scipy import misc

class Operation(object):
    def __init__(self, probability):
        self.probability = probability

    def __str__(self):
        return self.__class__.__name__

    def perform_operation(self, img):
        raise RuntimeError("Illegal call to base class.")


class Distort(Operation):
    def __init__(self, probability, grid_width, grid_height, magnitude):
        Operation.__init__(self, probability)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.magnitude = abs(magnitude)
        self.randomise_magnitude = True
    def perform_operation(self, img):
        # h, w = img.shape[:2]
        w, h = img.size
        horizontal_tiles = self.grid_width
        vertical_tiles = self.grid_height

        width_of_square = w // horizontal_tiles
        height_of_square = h // vertical_tiles

        width_of_last_square = w - (width_of_square * (horizontal_tiles - 1))
        height_of_last_square = h - (height_of_square * (vertical_tiles - 1))

        dimensions = []

        for vertical_tile in range(vertical_tiles):
            for horizontal_tile in range(horizontal_tiles):
                if vertical_tile == (vertical_tiles - 1) and horizontal_tile == (horizontal_tiles - 1):
                    dimensions.append([horizontal_tile * width_of_square,
                                       vertical_tile * height_of_square,
                                       width_of_last_square + (horizontal_tile * width_of_square),
                                       height_of_last_square + (height_of_square * vertical_tile)])
                elif vertical_tile == (vertical_tiles - 1):
                    dimensions.append([horizontal_tile * width_of_square,
                                       vertical_tile * height_of_square,
                                       width_of_square + (horizontal_tile * width_of_square),
                                       height_of_last_square + (height_of_square * vertical_tile)])
                elif horizontal_tile == (horizontal_tiles - 1):
                    dimensions.append([horizontal_tile * width_of_square,
                                       vertical_tile * height_of_square,
                                       width_of_last_square + (horizontal_tile * width_of_square),
                                       height_of_square + (height_of_square * vertical_tile)])
                else:
                    dimensions.append([horizontal_tile * width_of_square,
                                       vertical_tile * height_of_square,
                                       width_of_square + (horizontal_tile * width_of_square),
                                       height_of_square + (height_of_square * vertical_tile)])

        # For loop that generates polygons could be rewritten, but maybe harder to read?
        # polygons = [x1,y1, x1,y2, x2,y2, x2,y1 for x1,y1, x2,y2 in dimensions]

        # last_column = [(horizontal_tiles - 1) + horizontal_tiles * i for i in range(vertical_tiles)]
        last_column = []
        for i in range(vertical_tiles):
            last_column.append((horizontal_tiles-1)+horizontal_tiles*i)

        last_row = range((horizontal_tiles * vertical_tiles) - horizontal_tiles, horizontal_tiles * vertical_tiles)

        polygons = []
        for x1, y1, x2, y2 in dimensions:
            polygons.append([x1, y1, x1, y2, x2, y2, x2, y1])

        polygon_indices = []
        for i in range((vertical_tiles * horizontal_tiles) - 1):
            if i not in last_row and i not in last_column:
                polygon_indices.append([i, i + 1, i + horizontal_tiles, i + 1 + horizontal_tiles])

        for a, b, c, d in polygon_indices:
            dx = random.randint(-self.magnitude, self.magnitude)
            dy = random.randint(-self.magnitude, self.magnitude)

            x1, y1, x2, y2, x3, y3, x4, y4 = polygons[a]
            polygons[a] = [x1, y1,
                           x2, y2,
                           x3 + dx, y3 + dy,
                           x4, y4]

            x1, y1, x2, y2, x3, y3, x4, y4 = polygons[b]
            polygons[b] = [x1, y1,
                           x2 + dx, y2 + dy,
                           x3, y3,
                           x4, y4]

            x1, y1, x2, y2, x3, y3, x4, y4 = polygons[c]
            polygons[c] = [x1, y1,
                           x2, y2,
                           x3, y3,
                           x4 + dx, y4 + dy]

            x1, y1, x2, y2, x3, y3, x4, y4 = polygons[d]
            polygons[d] = [x1 + dx, y1 + dy,
                           x2, y2,
                           x3, y3,
                           x4, y4]

        generated_mesh = []
        for i in range(len(dimensions)):
            generated_mesh.append([dimensions[i], polygons[i]])
        
        # return cv2.remap(img, np.array(dimensions), np.array(polygons), cv2.INTER_CUBIC)

        return Image.transform(img.size, Image.MESH, generated_mesh, resample=Image.BICUBIC)

class Vignette(Operation):
    def __init__(self, probability, min_vignetting, max_vignetting):
        Operation.__init__(self, probability)
        self.min_vignetting = min_vignetting
        self.max_vignetting = max_vignetting

    def perform_operation(self, img):
        h, w = img.shape
        h_gk_size = random.choice(list(range(self.min_vignetting,self.max_vignetting, 2)))
        w_gk_size = random.choice(list(range(self.min_vignetting,self.max_vignetting, 2)))
        h_gk = cv2.getGaussianKernel(h,h_gk_size)
        w_gk = cv2.getGaussianKernel(w,w_gk_size)
        c = h_gk*w_gk.T
        d = c/c.max()
        e = img*d
        
        return e
if __name__ == '__main__':
    # ds = Distort(1.0, 3, 3, 4)
    ds = Vignette(1.0, 80, 100)
    for i in range(1, 31):
        img = Image.open('a/{}.png'.format(i))
        img = np.asarray(img)
        img = ds.perform_operation(img)
        img = np.asarray(img)
        misc.imsave('a/{}_after.png'.format(i), img)