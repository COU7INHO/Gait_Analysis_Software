import cv2
import numpy as np
from time import time


net = cv2.dnn.readNet("/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_training_last.weights", "/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_testing.cfg")

classes = ["Marker"]

camera = cv2.VideoCapture("/Users/tiagocoutinho/Desktop/short.MOV")
loop_time = time()

layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

tracker = cv2.TrackerKCF_create()

while camera.isOpened(): 

    ret, frame = camera.read()

    fps = 1/(time() - loop_time)
    loop_time = time()
    
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
                
                cv2.circle(frame, (int(x), int(y)), 5, (255, 50, 10), -1 )
                
                boxes.append([x1, y1, x2, y2])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    for i in range(len(boxes)):
        if i in indexes:
            x1, y1, x2, y2 = boxes[i]

            w = x2 - x1
            h = y2 - y1

            tracking = tracker.init(frame, boxes[i])

            if tracking:
                ok_update, bbox = tracker.update(frame, boxes[i])
                if ok_update:
                    print("Tracking...")
                    cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 3)

            else: 
                print("Not tracking")
                cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 3)

    cv2.putText(frame, f"FPS: {str(round(fps, 3))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 3)
    cv2.imshow("Detecting markers...", frame)
    
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()