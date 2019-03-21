""" Creates a section where the pixmap is being displayed and where
    the logic to detec objects over tensorflow is going to connect

    __author__ = Caglar Özel
"""

# pylint: disable=line-too-long
# pylint: disable=no-self-use

import os
import cv2

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QSlider
from PyQt5.QtGui import QPixmap, QImage

from helper import media_helper
from tf_detection import image_detection
from gui.gui_elements.common import file_manager


class ImageSection(QGridLayout):
    """ Class of ImageSection """

    def __init__(self):
        super().__init__()
        self.media_helper = media_helper.MediaHelper()
        self.img_detector = image_detection.TFImageDetection()

        # Private variables
        self.current_state = ""
        self.current_media = ""
        self.current_image = None
        self.timer = None
        self.chosen_image_directory = ""

        self.tree_view_width = 250
        self.current_width, self.current_height = 640, 480

        self.create_tree_view_layout()
        self.image_layout = QVBoxLayout()
        self.create_image_widget()

        self.addLayout(self.tree_view_layout, 1, 1)
        self.addLayout(self.image_layout, 1, 2)

    def clear_layout(self, layout):
        if layout is not None:
            for i in range(layout.count()):
                child = layout.itemAt(i)

                if child is not None and child.widget() is not None:
                    layout.itemAt(i).widget().deleteLater()
                else:
                    self.clear_layout(layout.itemAt(i))

    def create_image_widget(self):
        self.current_state = 'image'
        self.clear_layout(self.image_layout)

        self.image_label = QLabel()
        self.image_label.setScaledContents(False)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(self.current_width, self.current_height)

        self.image_layout.addWidget(self.image_label)

    def create_media_player(self):
        self.current_state = 'video'
        self.clear_layout(self.image_layout)

        self.video_label = QLabel()
        self.video_label.setScaledContents(False)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(self.current_width, self.current_height)

        video_layout = QHBoxLayout()
        video_layout.addWidget(self.video_label)

        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setText('Play')
        self.play_button.clicked.connect(self.play)

        self.position_slider = QSlider(Qt.Horizontal)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.position_slider)

        self.image_layout.addLayout(video_layout)
        self.image_layout.addLayout(button_layout)

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
            if self.media_helper.is_image(self.current_media):
                self.draw_image(self.current_media, True)
            # if self.media_helper.is_video(self.current_media):
            # self.play_video(self.current_media, width - self.tree_view_width, height, True)

    def show_media(self, media_path):
        """ Draw the selected pixmap """
        self.current_media = media_path

        if self.current_media != "" and os.path.isfile(self.current_media):
            if self.media_helper.is_image(media_path):
                if (self.current_state != 'image'):
                    self.create_image_widget()
                self.draw_image(media_path)
            elif self.media_helper.is_video(media_path):
                if (self.current_state != 'video'):
                    self.create_media_player()
                self.play_video(media_path)

    def draw_image(self, media_path, resize_event=False):
        """ Draw the pixmap on the QLabel Object and display it """
        image = cv2.imread(media_path)

        if self.media_helper.is_grayscale(image):
            image = self.media_helper.convert_grayscale_to_rgb(image)

        if not resize_event:
            # Numpy array containing the rgb pixels
            self.current_image = self.img_detector.object_detection(image)

        #if self.img_detector is None:
        #    self.current_image = image

        img_height, img_width, channels = self.current_image.shape

        image = QImage(
            self.current_image, img_width, img_height, self.current_image.strides[0],
            QImage.Format_RGB888
        ).scaled(QSize(self.current_width, self.current_height), Qt.KeepAspectRatio).rgbSwapped()

        pixmap = QPixmap(image).scaled(QSize(self.current_width, self.current_height), Qt.KeepAspectRatio)

        self.image_label.setPixmap(pixmap)

    def play_video(self, video_path, resize_event=False):
        """ Render the Video in QLabel Object """
        self.playing_video = False
        self.play_button.setText('Play')

        if self.timer is not None:
            self.timer.stop()

        self.play_button.setEnabled(True)
        self.video_capture = cv2.VideoCapture(video_path)

        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.current_height)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.current_width)

        self.duration_changed(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.position_slider.sliderMoved.connect(self.position_changed)

    def update_frame(self):
        ret, frame = self.video_capture.read()

        q_format = QImage.Format_Indexed8

        image = self.img_detector.object_detection(frame)
        height, width, channels = frame.shape

        if channels == 4:
            q_format = QImage.Format_RGBA8888
        else:
            q_format = QImage.Format_RGB888

        image = QImage(frame, width, height, frame.strides[0], q_format).scaled(
            QSize(self.current_width, self.current_height - 100), Qt.KeepAspectRatio
        ).rgbSwapped()

        self.video_label.setPixmap(
            QPixmap.fromImage(image).scaled(
                QSize(self.current_width, self.current_height - 200), Qt.KeepAspectRatio
            )
        )

    def play(self):
        self.playing_video = not self.playing_video
        if self.playing_video is True:
            self.play_button.setText('Pause')
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(1)
        else:
            self.timer.stop()
            self.play_button.setText('Play')

    def get_selected_media(self, chosen_item):
        """ return the selected item from the side section """
        self.show_media(chosen_item["file_path"])

    def position_changed(self, position):
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, position - 1)
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)
        self.position_slider.setValue(0)

    def set_image_dir(self, chosen_dir):
        """ Set the side view with the chosen directory """
        self.chosen_image_directory = chosen_dir["dir_path"]
        self.tree_obj["file_manager"].setRootIndex(
            self.tree_obj["file_model"].index(chosen_dir["dir_path"])
        )
