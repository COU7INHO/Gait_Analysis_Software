
import cv2
import numpy as np
from time import time
from detector_function import markerDetection

names = ["Shoulder", "Trochanter", "Knee", "Ankle", "V_Metatarsal"]

# Number of markers to detect and track
n_markers = 3

#camera = cv2.VideoCapture("/Users/tiagocoutinho/Desktop/3markers.mov")
camera = cv2.VideoCapture(0)

loop_time = time()

# Read first frame
ret, frame = camera.read()

# Method to detect the markers on the first frame
frame, boxes, indexes = markerDetection(frame)

# Create the multiTracker to track multiple markers
multiTracker = cv2.legacy.MultiTracker_create()

# Add a tracker to each bounding box
for box in boxes:
    multiTracker.add(cv2.legacy.TrackerCSRT_create(), frame, box)

print("\nStarting programme...\n")

while camera.isOpened():

    success, frame = camera.read()

    if success == False:
        break
    
    # Analyze the FPS rate
    fps = 1/(time() - loop_time)
    loop_time = time()
    
    # Remove boxes equal to [0, 0, 0, 0] -> Empty boxes
    boxes = [box for box in boxes if np.any(box != [0, 0, 0, 0])]

    # If len(boxes) doesn't match the number of markers it runs the detector
    if len(boxes) != n_markers :
        if n_markers - len(boxes) == 1:
            cv2.putText(frame, "1 marker missing", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        elif n_markers - len(boxes) == -1:
            cv2.putText(frame, "1 marker in excess", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        elif n_markers - len(boxes) > 1:
            cv2.putText(frame, f"{int(n_markers - len(boxes))} markers missing", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        elif n_markers - len(boxes) < -1:
            cv2.putText(frame, f"{abs(int(n_markers - len(boxes)))} markers in excess", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

        # Run the detector
        frame, boxes, indexes = markerDetection(frame)
        # Update the multiTracker with the new bounding boxes
        multiTracker = cv2.legacy.MultiTracker_create()
        for box in boxes:
            multiTracker.add(cv2.legacy.TrackerCSRT_create(), frame, box)
    else:
        cv2.putText(frame, "Tracking", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 3)
        # Update the tracker
        tracking, boxes = multiTracker.update(frame)

    sorted_boxes = []

    # Get the x, y coordinates, width and heigh of each bounding box
    for i, newbox in enumerate(boxes):
        x = int(newbox[0])
        y = int(newbox[1])
        w = int(newbox[2])
        h = int(newbox[3])

        # Get the center point of each bounding box 
        center = (x + w//2, y + h//2)
        y_coord = center[1]

        # Append a tuple containing the newbox object, its y coordinate in the center point, and its ID to the sorted_boxes list
        sorted_boxes.append((y_coord, i))

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
        cv2.circle(frame, center, 6, (255, 0, 0), -1)
    
    # Sort the sorted_boxes list by the y coordinate in the center point
    sorted_boxes = sorted(sorted_boxes, key=lambda x: x[1])

    # Assign names to the markers in the sorted order
    for i, (y_coord, id) in enumerate(sorted_boxes):
        if i <= len(names):
            name = names[i]
        else:
            name = f"Marker {i}"
        print(f"Marker {id}: {name}, y: {y_coord}")

        for i, newbox in enumerate(boxes):
            x = int(newbox[0])
            y = int(newbox[1])
            w = int(newbox[2])
            h = int(newbox[3])
            cv2.putText(frame, f"{i}: {names[i]}", (x, y - 20), 1, cv2.FONT_HERSHEY_COMPLEX, (0, 255, 128), 3)

    cv2.putText(frame, f"FPS: {str(round(fps, 2))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
    cv2.putText(frame, f"Markers: {str(len(boxes))}", (10, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
    cv2.imshow('Gait analysis', frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break 

camera.release()
cv2.destroyAllWindows()