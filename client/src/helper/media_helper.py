""" This is a Class which will handle checking Images towards validity and
    converting grayscale images to proper rgb ones so Tensorflow can perform object
    detection on them.

    __author__ = Caglar Özel
"""

import os
import numpy


class MediaHelper():
    def __init__(self):
        pass

    def is_grayscale(self, image):
        """ Check if image is greyscale """
        if len(image.shape) < 3:
            return True
        return False

    def is_image(self, media_path):
        """ check if file is image """
        extension = os.path.splitext(media_path)[1]
        if extension == '.jpg' or extension == '.png' or extension == '.jpeg':
            return True
        return False

    def is_video(self, media_path):
        """ check if file is video """
        extension = os.path.splitext(media_path)[1]
        if extension == '.mp4':
            return True
        return False

    def convert_grayscale_to_rgb(self, image):
        return numpy.stack((image, ) * 3, axis=-1)
