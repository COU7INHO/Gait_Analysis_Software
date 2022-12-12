import cv2
import numpy as np
from time import time

net = cv2.dnn.readNet("/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_training_last.weights", "/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_testing.cfg")

classes = ["Marker"]

#camera = cv2.VideoCapture("/Users/tiagocoutinho/Desktop/video.mov")
camera = cv2.VideoCapture(0)

loop_time = time()

layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

ret, frame = camera.read()

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

        if confidence > 0.3:
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
            
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        #cv2.putText(frame, str(i), (x, y + 30), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2)

multiTracker = cv2.legacy.MultiTracker_create()

for box in boxes:
  multiTracker.add(cv2.legacy.TrackerKCF_create(), frame, box)

while camera.isOpened():

    success, frame = camera.read()

    fps = 1/(time() - loop_time)
    loop_time = time()
    
    if not success:
        print("There are no cameras available")

    print("Tracking markers...")
    success, boxes = multiTracker.update(frame)

    for i, newbox in enumerate(boxes):
        x = int(newbox[0])
        y = int(newbox[1])
        w = int(newbox[2])
        h = int(newbox[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2, 3)
        cv2.putText(frame, str(i), (x, y - 20), 1, cv2.FONT_HERSHEY_COMPLEX, (255, 150, 0), 2)
    cv2.putText(frame, f"FPS: {str(round(fps, 2))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 3)
    cv2.imshow('MultiTracker', frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()