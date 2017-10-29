try:
    from .meta import Operation
except Exception:
    from meta import Operation
from PIL import Image
import numpy as np
import math
import cv2

class Affine(Operation):
    _fields = ['degree', 'direction']
    def perform_on_image(self, img):
        def from_Augmentor(image, degree, direction):
            """
            Shears the passed image according to the parameters defined during 
            instantiation, and returns the sheared image.
            
            :param image: The image to shear.
            :type image: PIL.Image
            :return: The sheared image of type PIL.Image
            """
            ######################################################################
            # Old version which uses SciKit Image
            ######################################################################
            # We will use scikit-image for this so first convert to a matrix
            # using NumPy
            # amount_to_shear = round(random.uniform(self.max_shear_left, self.max_shear_right), 2)
            # image_array = np.array(image)
            # And here we are using SciKit Image's `transform` class.
            # shear_transformer = transform.AffineTransform(shear=amount_to_shear)
            # image_sheared = transform.warp(image_array, shear_transformer)
            #
            # Because of warnings
            # with warnings.catch_warnings():
            #     warnings.simplefilter("ignore")
            #     return Image.fromarray(img_as_ubyte(image_sheared))
            ######################################################################

            width, height = image.size

            # For testing.
            # max_shear_left = 20
            # max_shear_right = 20

            angle_to_shear = degree

            # We use the angle phi in radians later
            phi = math.tan(math.radians(angle_to_shear))

            # Alternative method
            # Calculate our offset when cropping
            # We know one angle, phi (angle_to_shear)
            # We known theta = 180-90-phi
            # We know one side, opposite (height of image)
            # Adjacent is therefore:
            # tan(theta) = opposite / adjacent
            # A = opposite / tan(theta)
            # theta = math.radians(180-90-angle_to_shear)
            # A = height / math.tan(theta)

            # Transformation matrices can be found here:
            # https://en.wikipedia.org/wiki/Transformation_matrix
            # The PIL affine transform expects the first two rows of
            # any of the affine transformation matrices, seen here:
            # https://en.wikipedia.org/wiki/Transformation_matrix#/media/File:2D_affine_transformation_matrix.svg

            if direction == 'x':
                # Here we need the unknown b, where a is
                # the height of the image and phi is the
                # angle we want to shear (our knowns):
                # b = tan(phi) * a
                shift_in_pixels = phi * height

                if shift_in_pixels > 0:
                    shift_in_pixels = math.ceil(shift_in_pixels)
                else:
                    shift_in_pixels = math.floor(shift_in_pixels)

                # For negative tilts, we reverse phi and set offset to 0
                # Also matrix offset differs from pixel shift for neg
                # but not for pos so we will copy this value in case
                # we need to change it
                matrix_offset = shift_in_pixels
                if angle_to_shear <= 0:
                    shift_in_pixels = abs(shift_in_pixels)
                    matrix_offset = 0
                    phi = abs(phi) * -1

                # Note: PIL expects the inverse scale, so 1/scale_factor for example.
                transform_matrix = (1, phi, -matrix_offset,
                                    0, 1, 0)

                image = image.transform((int(round(width + shift_in_pixels)), height),
                                        Image.AFFINE,
                                        transform_matrix,
                                        Image.BICUBIC)

                image = image.crop((abs(shift_in_pixels), 0, width, height))

                return image.resize((width, height), resample=Image.BICUBIC)

            elif direction == "y":
                shift_in_pixels = phi * width

                matrix_offset = shift_in_pixels
                if angle_to_shear <= 0:
                    shift_in_pixels = abs(shift_in_pixels)
                    matrix_offset = 0
                    phi = abs(phi) * -1

                transform_matrix = (1, 0, 0,
                                    phi, 1, -matrix_offset)

                image = image.transform((width, int(round(height + shift_in_pixels))),
                                        Image.AFFINE,
                                        transform_matrix,
                                        Image.BICUBIC)

                image = image.crop((0, abs(shift_in_pixels), width, height))

                return image# image.resize((width, height), resample=Image.BICUBIC)
        img_pil = Image.fromarray(img)
        res = from_Augmentor(img_pil, self.degree, self.direction)
        res = np.array(res)
        return res

class Rotate(Operation):
    _fields = ['degree', 'mode']
    def perform_on_image(self, img):
        def largest_rotated_rect(w, h, angle):
            """
            Get largest rectangle after rotation.
            http://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
            """
            angle = angle / 180.0 * math.pi
            if w <= 0 or h <= 0:
                return 0, 0

            width_is_longer = w >= h
            side_long, side_short = (w, h) if width_is_longer else (h, w)

            # since the solutions for angle, -angle and 180-angle are all the same,
            # if suffices to look at the first quadrant and the absolute values of sin,cos:
            sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
            if side_short <= 2. * sin_a * cos_a * side_long:
                # half constrained case: two crop corners touch the longer side,
                #   the other two corners are on the mid-line parallel to the longer line
                x = 0.5 * side_short
                wr, hr = (x / sin_a, x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
            else:
                # fully constrained case: crop touches all 4 sides
                cos_2a = cos_a * cos_a - sin_a * sin_a
                wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a - w * sin_a) / cos_2a
            return int(np.round(wr)), int(np.round(hr))
        img_pil = Image.fromarray(img)
        if self.mode == 'expand':
            after = img_pil.rotate(self.degree, expand = 1)
            res = np.array(after)
        elif self.mode == 'crop_valid':
            center = (img.shape[1] * 0.5, img.shape[0] * 0.5)
            rot_m = cv2.getRotationMatrix2D((center[0] - 0.5, center[1] - 0.5), self.degree, 1)
            ret = cv2.warpAffine(img, rot_m, img.shape[1::-1])
            if img.ndim == 3 and ret.ndim == 2:
                ret = ret[:, :, np.newaxis]
            neww, newh = largest_rotated_rect(ret.shape[1], ret.shape[0], self.degree)
            neww = min(neww, ret.shape[1])
            newh = min(newh, ret.shape[0])
            newx = int(center[0] - neww * 0.5)
            newy = int(center[1] - newh * 0.5)
            # print(ret.shape, deg, newx, newy, neww, newh)
            res = ret[newy:newy + newh, newx:newx + neww]
            # after = img_pil.rotate(self.degree, expand = 1)
            # h, w = img.shape[:2]
            # after_w, after_h = after.size
            # print(after.size)
            # neww, newh = largest_rotated_rect(after_w, after_h, self.degree)
            # neww = min(neww, after_w)
            # newh = min(newh, after_h)
            # newx = int((w - neww) * 0.5)
            # newy = int((h - newh) * 0.5)
            # res = np.array(after)[newy:newy + newh, newx:newx + neww]
            # print(newh, newx)
        else:
            after = img_pil.rotate(self.degree)
            res = np.array(after)
        return res

