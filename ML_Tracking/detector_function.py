import cv2
import numpy as np

# This script is used to run the yolov3 model and detect the markers
def markerDetection(frame):
    net = cv2.dnn.readNet("/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_training_last.weights", "/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_testing.cfg")
    classes = ["Marker"]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

    if frame is not None:
        height, width, channels = frame.shape

        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                x, y, w, h = detection[0:4] * np.array([width, height, width, height])
                x1 = int(x - w/2)
                y1 = int(y - h/2)
                x2 = int(x + w/2)
                y2 = int(y + h/2)
                w = x2 - x1
                h = y2 - y1

                boxes.append([x1, y1, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                
    #indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    return frame, boxes, indexes