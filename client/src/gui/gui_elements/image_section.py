""" Creates a section where the pixmap is being displayed and where
    the logic to detec objects over tensorflow is going to connect

    __author__ = Caglar Özel
"""

# pylint: disable=line-too-long
# pylint: disable=no-self-use

import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel

from helper import config_getter
from tf_detection import tensorflow_session
from tf_detection import image_detection


class ImageSection(QHBoxLayout):
    """ Class of ImageSection """

    def __init__(self):
        super().__init__()

        # Private variables
        self.current_media = ""
        self.tree_view_width = 250
        self.current_raw_image = None
        self.current_width, self.current_height = 640, 480

        self.img_detector = image_detection.TFImageDetection()

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setMinimumSize(self.current_width, self.current_height)
        self.img_label.setScaledContents(False)

        self.addWidget(self.img_label)

    def resize_update(self, width, height):
        """ Update method to handle Resize events """
        self.current_width = width - 250
        self.current_height = height
        if self.current_media != "":
            if self.is_image(self.current_media):
                self.draw_image(self.current_media, width - self.tree_view_width, height, True)
            elif self.is_video(self.current_media):
                self.play_video(self.current_media, width - self.tree_view_width, height, True)

    def show_media(self, media_path):
        """ Draw the selected pixmap """
        self.current_media = media_path

        if self.current_media != "" and os.path.isfile(self.current_media):
            if self.is_image(media_path):
                self.draw_image(media_path, self.current_width, self.current_height)
            elif self.is_video(media_path):
                self.play_video(media_path, self.current_width, self.current_height)

    def draw_image(self, media_path, width, height, resize_event=False):
        """ Draw the pixmap on the QLabel Object and display it """
        # Numpy array containing the rgb pixels

        if not resize_event:
            self.current_raw_image = self.img_detector.object_detection(media_path)

        img_height, img_width, channels = self.current_raw_image.shape
        bytes_per_line = channels * img_width

        image = QImage(
            self.current_raw_image, img_width, img_height, bytes_per_line, QImage.Format_RGB888
        ).scaled(QSize(width, height), Qt.KeepAspectRatio).rgbSwapped()

        pixmap = QPixmap(image).scaled(QSize(width, height), Qt.KeepAspectRatio)

        self.img_label.setPixmap(pixmap)
        self.img_label.show()

    def play_video(self, video_path, width, height, resize_event=False):
        """ Render the Video in QLabel Object """
        #TODO: implement this to display videos in qt
        print(video_path, ' ', width, '  ', height)

    def is_image(self, media_path):
        """ check if file is image """
        extension = os.path.splitext(media_path)[1]

        if extension == 'jpg' or 'png' or 'jpeg':
            return True

        return False

    def is_video(self, media_path):
        """ check if file is video """
        extension = os.path.splitext(media_path)[1]

        if extension == 'mp4':
            return True

        return False
