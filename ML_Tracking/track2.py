import cv2
import numpy as np
import imutils
from time import time


net = cv2.dnn.readNet("/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_training_last.weights", "/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_testing.cfg")

classes = ["Marker"]

camera = cv2.VideoCapture("/Users/tiagocoutinho/Desktop/markers.MOV")
loop_time = time()

layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

while camera.isOpened():

    ret, frame = camera.read()
    frame = imutils.resize(frame, width=720)

    fps = 1/(time() - loop_time)
    loop_time = time()
    
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
    tracker = cv2.TrackerKCF_create()

    for i in range(len(boxes)):

        x1, y1, x2, y2 = boxes[i]
        success = tracker.init(frame, boxes[i])
        
        if success:
            print("success")
            success, bbox = tracker.update(frame)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        else:
            print("no success")
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

    cv2.putText(frame, f"FPS: {str(round(fps, 3))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 3)
    cv2.imshow("Detecting markers...", frame)
    
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()


'''https://stackoverflow.com/questions/48886532/how-to-use-opencv-tracker-parameters-without-selecting-a-roi'''