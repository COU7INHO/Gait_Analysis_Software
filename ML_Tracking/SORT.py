import cv2
import numpy as np
from time import time

# Import SORT tracker
from sort.sort import Sort

# Set SORT tracker parameters
max_age = 1  # Number of frames to keep track of a particular object
min_hits = 1  # Minimum number of detections before considering an object to be tracked
tracker = Sort(max_age=max_age, min_hits=min_hits)

# Load the YOLOv3 model
net = cv2.dnn.readNet("/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_training_last.weights", "/Users/tiagocoutinho/Desktop/Gait_Software/ML_Tracking/yolov3_testing.cfg")

# Define the class labels
classes = ["Marker"]

# Open the video file
camera = cv2.VideoCapture("/Users/tiagocoutinho/Desktop/3markers.mov")

# Get the layer names of the YOLOv3 model
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

loop_time = time()
# Initialize variables for tracking
boxes = []  # Bounding boxes of the detected objects
confidences = []  # Confidences of the detections
class_ids = []  # Class IDs of the detected objects

while camera.isOpened():
    # Read a frame from the video
    ret, frame = camera.read()

    # Check if the frame was correctly read
    if not ret:
        break

    # Calculate the frame rate
    fps = 1/(time() - loop_time)
    loop_time = time()

    # Get the dimensions of the frame
    height, width, channels = frame.shape

    # Convert the frame to a blob and pass it through the YOLOv3 model
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Loop through the detections
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Consider only detections with confidence above a certain threshold
            if confidence > 0.3:
                # Get the bounding box coordinates and dimensions
                x, y, w, h = detection[0:4] * np.array([width, height, width, height])
                x1 = int(x - w/2)
                y1 = int(y - h/2)
                x2 = int(x + w/2)
                y2 = int(y + h/2)

                # Draw a circle at the center of the detection
                cv2.circle(frame, (int(x), int(y)), 5, (255, 50, 10), -1)

                # Add the detection to the list of bounding boxes, confidences, and class IDs
                boxes.append([x1, y1, x2, y2])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Use the SORT tracker to track the objects
    tracks = tracker.update(np.array(boxes))

    # Loop through the tracked objects
    for track in tracks:
        # Get the bounding box coordinates and dimensions
        x1, y1, x2, y2 = track[:4].astype(int)

        # Draw a rectangle around the tracked object
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        # Get the object ID and class label
        object_id = int(track[4])
        #!class_label = classes[int(track[5])]

        # Put the object ID and class label on the frame
        cv2.putText(frame, f"ID: {object_id}", (x1, y1-10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 3)
        #!cv2.putText(frame, f"Class: {class_label}", (x1, y1-30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 3)

    # Display the frame with the tracked objects
    cv2.putText(frame, f"FPS: {str(round(fps, 3))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 3)
    cv2.imshow("Tracking markers...", frame)

    # Check for user input to stop the program
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the video capture and destroy the windows
camera.release()
cv2.destroyAllWindows()

