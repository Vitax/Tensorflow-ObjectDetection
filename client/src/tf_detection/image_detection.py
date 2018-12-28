"""
    Script to run object detection on a image using the Tensorflow Framework,
    this will return the Image analysed with drawn bounding boxes on found objects

    __author__=Caglar Özel
"""

import cv2
import numpy

from helper import config_getter
from tf_detection import tensorflow_session
from object_detection.utils import visualization_utils


class TFImageDetection():
    """ Class to detect objects in images using the Tensorflow Framework

        params:
        -------
        session:
            Tensorflow session which is going to be used for object detection
        tensor_objects:
            Objects created by the Tensorflow session which is required for the Object Detection
    """

    def __init__(self):
        # Get Configration file
        config_file_path = config_getter.get_config_file()
        self.config_content = config_getter.get_config_file_content(config_file_path)

    def object_detection(self, file_path, threshhold=0.5):
        """ Performs the Object detection with the given threshold """
        # Intitializes the tensorflow model
        tensor_model = tensorflow_session.TensorflowSession(self.config_content)
        session = tensor_model.session
        tensor_objects = tensor_model.tensor_object

        image = cv2.imread(file_path)

        # Expand dimension of the rgb array to use it in tensorflow detection
        image_expanded = numpy.expand_dims(image, axis=0)

        (boxes, scores, classes, num) = session.run(
            [
                tensor_objects["boxes"], tensor_objects["scores"], tensor_objects["classes"],
                tensor_objects["detections"]
            ],
            feed_dict={tensor_objects["tensor"]: image_expanded}
        )

        visualization_utils.visualize_boxes_and_labels_on_image_array(
            image,
            numpy.squeeze(boxes),
            numpy.squeeze(classes).astype(numpy.int32),
            numpy.squeeze(scores),
            tensor_objects["category_index"],
            use_normalized_coordinates=True,
            line_thickness=2,
            min_score_thresh=threshhold
        )

        return image
