""" Creates a section where the pixmap is being displayed and where
    the logic to detec objects over tensorflow is going to connect

    __author__ = Caglar Özel
"""

# pylint: disable=line-too-long
# pylint: disable=no-self-use

import os
import cv2

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton

from tf_detection import image_detection
from gui.gui_elements.common import file_manager


class ImageSection(QGridLayout):
    """ Class of ImageSection """

    def __init__(self):
        super().__init__()

        # Private variables
        self.current_media = ""
        self.chosen_image_directory = ""
        self.tree_view_width = 250
        self.current_raw_image = None
        self.current_width, self.current_height = 640, 480

        self.img_detector = image_detection.TFImageDetection()

        self.create_image_layout()
        self.create_tree_view_layout()

        self.addLayout(self.tree_view_layout, 1, 1)
        self.addLayout(self.image_layout, 1, 2)

    def create_image_layout(self):
        self.image_layout = QHBoxLayout()

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setMinimumSize(self.current_width, self.current_height)
        self.img_label.setScaledContents(False)

        self.image_layout.addWidget(self.img_label)

    def create_tree_view_layout(self):
        self.file_manager = file_manager.FileManager(self.tree_view_width)

        self.tree_view_layout = QVBoxLayout()
        self.tree_view_layout.setAlignment(Qt.AlignLeft)

        button = QPushButton()
        button.setText('Open Image Folder')
        button.clicked.connect(
            lambda x: self.file_manager.create_tree_view_popup("", self.set_image_dir, True)
        )

        self.tree_view_layout.addWidget(button)

        self.tree_obj = self.file_manager.create_tree_view("/home", self.get_selected_media)
        self.tree_view_layout.addWidget(self.tree_obj["file_manager"])

    def resize_update(self, width, height):
        """ Update method to handle Resize events """
        self.current_width = width - self.tree_view_width
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
            self.current_raw_image = self.img_detector.object_detection(cv2.imread(media_path))

        img_height, img_width, channels = self.current_raw_image.shape

        image = QImage(
            self.current_raw_image, img_width, img_height, self.current_raw_image.strides[0], QImage.Format_RGB888
        ).scaled(QSize(width, height), Qt.KeepAspectRatio).rgbSwapped()

        pixmap = QPixmap(image).scaled(QSize(width, height), Qt.KeepAspectRatio)

        self.img_label.setPixmap(pixmap)

    def play_video(self, video_path, width, height, resize_event=False):
        """ Render the Video in QLabel Object """
        #TODO: implement this to display videos in qt

        if not resize_event:
            print('resize the video without doing anything else')

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

    def set_image_dir(self, chosen_dir):
        """ Set the side view with the chosen directory """
        self.chosen_image_directory = chosen_dir["dir_path"]
        self.tree_obj["file_manager"].setRootIndex(
            self.tree_obj["file_model"].index(chosen_dir["dir_path"])
        )

    def get_selected_media(self, chosen_item):
        """ return the selected item from the side section """
        self.show_media(chosen_item["file_path"])
