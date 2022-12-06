import cv2
import numpy as np
import imutils
from time import time
import math


# Load Yolo
net = cv2.dnn.readNet("/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_training_last.weights", "/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_testing.cfg")

# Name custom object
classes = ["Marker"]

# Images path
camera = cv2.VideoCapture("/Users/tiagocoutinho/Desktop/marcadores.MOV")
loop_time = time()

layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

center_points_prev_frame = []
tracking_objects = {}
track_id = 0

while camera.isOpened():

    ret, frame = camera.read()
    frame = imutils.resize(frame, width=720)

    fps = 1/(time() - loop_time)
    loop_time = time()
    
    center_points_cur_frame = []

    # Loading image
    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outputs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []

    for out in outputs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                x, y, w, h = detection[0:4] * np.array([width, height, width, height])
                x1 = int(x - w/2)
                y1 = int(y - h/2)
                x2 = int(x + w/2)
                y2 = int(y + h/2)
                
                center_points_cur_frame.append((int(x), int(y)))
                boxes.append([x1, y1, x2, y2])
                confidences.append(float(confidence))
                class_ids.append(class_id)


        for point in center_points_cur_frame:
            for point2 in center_points_prev_frame:
                distance = math.hypot(point2[0] - point[0], point2[1 ] - point[1])

                if distance < 10:
                    tracking_objects[track_id] = point
                    track_id += 1

        for object_id, point in tracking_objects.items():
            cv2.circle(frame, point, 5, (255, 50, 10), -1 )
            cv2.putText(frame, str(object_id), (point[0], point[1] - 40), 1, cv2.FONT_HERSHEY_COMPLEX, (12, 255, 0), 2)
        

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x1, y1, x2, y2 = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

            #?cv2.putText(frame, label, (x, y - 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

    cv2.putText(frame, f"FPS: {str(round(fps, 3))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 3)
    cv2.imshow("Detecting markers...", frame)

    center_points_prev_frame = center_points_cur_frame.copy()
    print("Center points current frame: ", center_points_cur_frame)
    print("Previous points current frame: ", center_points_prev_frame)


    key = cv2.waitKey(0)

    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()