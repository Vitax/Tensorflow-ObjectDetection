""" This Class will create the Layout for the Webcam section of the
    Application.

    __author = Caglar Özel
"""

import cv2

from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout

from tf_detection import image_detection


class CameraSection(QGridLayout):
    def __init__(self):
        super().__init__()

        self.capture_camera = False

        self.current_width, self.current_height = 640, 480
        self.button_layout = self.create_camera_label()
        self.camera_layout = self.create_button_layout()
        self.img_detector = image_detection.TFImageDetection()

        self.addLayout(self.button_layout, 2, 1)
        self.addLayout(self.camera_layout, 1, 1)

    def resize_update(self, width, height):
        """ Update method to handle Resize events """
        self.current_width = width
        self.current_height = height

    def create_camera_label(self):
        camera_layout = QHBoxLayout()
        self.camera_label = QLabel()

        self.camera_label.setMinimumSize(self.current_width, self.current_height)
        self.camera_label.setScaledContents(False)
        camera_layout.addWidget(self.camera_label)

        return camera_layout

    def create_button_layout(self):
        button_layout = QHBoxLayout()

        start_webcam_button = self.create_button("Start Webcam")
        start_webcam_button.clicked.connect(self.start_webcam)

        stop_webcam_button = self.create_button("Stop Webcam")
        stop_webcam_button.clicked.connect(self.stop_webcam)

        button_layout.addWidget(start_webcam_button)
        button_layout.addWidget(stop_webcam_button)

        return button_layout

    def create_button(self, title):
        button = QPushButton()
        button.setText(title)

        return button

    def start_webcam(self):
        self.capture_camera = True

        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.current_height)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.current_width)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret, frame = self.capture.read()

        q_format = QImage.Format_Indexed8

        image = self.img_detector.object_detection(frame)
        width, height, channels = frame.shape

        if channels == 4:
            q_format = QImage.Format_RGBA8888
        else:
            q_format = QImage.Format_RGB888

        image = QImage(frame, height, width, frame.strides[0], q_format).scaled(
            QSize(self.current_width, self.current_height), Qt.KeepAspectRatio
        ).rgbSwapped()

        self.camera_label.setPixmap(
            QPixmap.fromImage(image).scaled(
                QSize(self.current_width, self.current_height), Qt.KeepAspectRatio
            )
        )

    def stop_webcam(self):
        self.capture_camera = False
        self.timer.stop()
        self.capture.release()
