"""This Class will create a Tensorflow session with all its required objects
    to perform a tensorflow object detection

    __author__ = Caglar Özel
"""

#pylint: disable=too-many-locals
#pylint: disable=too-few-public-methods

import tensorflow

from object_detection.utils import label_map_util


class TensorflowSession():
    """ Class which will create the Tensorflow Session & Object """

    session = None
    tensor_object = {}

    def __init__(self, tensorflow_configuration):
        """ Initializes the Class containing a Tensorflow _session """
        label_map = label_map_util.load_labelmap(tensorflow_configuration["label_map"])

        categories = label_map_util.convert_label_map_to_categories(
            label_map,
            max_num_classes=int(int(tensorflow_configuration["num_classes"])),
            use_display_name=True
        )

        category_index = label_map_util.create_category_index(categories)

        detection_graph = tensorflow.Graph()

        with detection_graph.as_default():
            graph_def = tensorflow.GraphDef()

            with tensorflow.gfile.GFile(tensorflow_configuration["inference_graph"], 'rb') as f:
                serialized_graph = f.read()
                graph_def.ParseFromString(serialized_graph)
                tensorflow.import_graph_def(graph_def, name="")

            self.session = tensorflow.Session(graph=detection_graph)

        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        tensorflow_objects = {
            "tensor": image_tensor,
            "boxes": detection_boxes,
            "scores": detection_scores,
            "classes": detection_classes,
            "detections": num_detections,
            "category_index": category_index
        }

        self.tensor_object = tensorflow_objects
