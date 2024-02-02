"""
MarkerDetection Class

This class defines a MarkerDetection object for detecting markers in a given frame using YOLO v3 (You Only Look Once) object detection.

Dependencies:
- cv2: OpenCV library for computer vision.

Attributes:
- detectFrame: The input frame to be processed for marker detection.
- confidenceValue: Confidence threshold for considering detected markers (default is 0.6).
- weightsFile: Path to the YOLO weights file.
- cfgFile: Path to the YOLO configuration file.
- net: YOLO neural network model.
- blob: Blob representation of the input frame.

Methods:
- __init__: Initializes the MarkerDetection object with input parameters.
- detect: Performs marker detection on the provided frame using YOLO.

Usage:
- Create an instance of the MarkerDetection class with the input frame and optional parameters.
- Call the detect() method to perform marker detection and obtain the results.

Note: Ensure that the YOLO weights file and configuration file paths are correctly specified.
"""

import cv2
import numpy as np


class MarkerDetection:
    def __init__(
        self,
        detectFrame,
        confidenceValue=0.6,
        weightsFile="/Users/tiagocoutinho/Desktop/Gait_Software/main_folder/yolov3_training_last.weights",
        cfgFile="/Users/tiagocoutinho/Desktop/Gait_Software/main_folder/yolov3_testing.cfg",
    ):
        """
        Initialize the MarkerDetection object.

        Parameters:
        - detectFrame: Input frame for marker detection.
        - confidenceValue: Confidence threshold for marker detection (default is 0.6).
        - weightsFile: Path to the YOLO weights file.
        - cfgFile: Path to the YOLO configuration file.
        """
        self.detectFrame = detectFrame
        self.confidenceValue = confidenceValue
        self.net = cv2.dnn.readNet(weightsFile, cfgFile)
        self.blob = None

    def detect(self):
        """
        Perform marker detection on the input frame using YOLO.

        Returns:
        - detectFrame: Processed frame with detected markers.
        - boxes: List of bounding boxes for detected markers.
        - indexes: Indexes of selected bounding boxes after non-maximum suppression.
        """
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        if self.detectFrame is not None:
            height, width, channels = self.detectFrame.shape

            self.blob = cv2.dnn.blobFromImage(
                self.detectFrame, 0.00392, (416, 416), (0, 0, 0), True, crop=False
            )

        self.net.setInput(self.blob)
        outs = self.net.forward(output_layers)

        class_ids = []
        confidences = []
        self.boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                self.confidenceValue = scores[class_id]

                if self.confidenceValue > 0.5:
                    x, y, w, h = detection[0:4] * np.array(
                        [width, height, width, height]
                    )
                    x1 = int(x - w / 2)
                    y1 = int(y - h / 2)
                    x2 = int(x + w / 2)
                    y2 = int(y + h / 2)
                    w = x2 - x1
                    h = y2 - y1

                    self.boxes.append([x1, y1, w, h])
                    confidences.append(float(self.confidenceValue))
                    class_ids.append(class_id)

        # indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        self.indexes = cv2.dnn.NMSBoxes(self.boxes, confidences, 0.5, 0.4)

        return self.detectFrame, self.boxes, self.indexes
