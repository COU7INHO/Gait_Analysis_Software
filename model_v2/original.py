
import cv2
import numpy as np
from time import time
from detector_function import markerDetection
from calc_angles import CalcAngles


# List of markers
names = ["Shoulder", "Trochanter", "Knee", "Ankle", "V_Metatarsal"]

# Initial settings
n_markers = 5
labels = True
draw_lines = True

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

first_ankle_angle = []
angle_stored = False

#*###################### Angles Lists ######################

hip_angles = []
knee_angles = []
ankle_angles = []

#*############################################
while camera.isOpened():

    success, frame = camera.read()
    if success == False:
        break
        
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

    sorted_yCoord = []
    centers = []
    prev_center = None

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
        sorted_yCoord.append((y_coord, i))

        # Append center point coordinate and index to centers list
        centers.append((center, i))

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
        cv2.circle(frame, center, 6, (255, 0, 0), -1)

        # If this is not the first bounding box, draw a line to the previous one
        if draw_lines:
            if prev_center is not None:
                cv2.line(frame, center, prev_center, (255, 255, 0), 2)
        
        # Define the new center point of each bounding box  
        prev_center = center

    # Sort the sorted_boxes list by the y coordinate in the center point
    sorted_yCoord = sorted(sorted_yCoord, key=lambda x: x[0])

    # Create center point coordinates lists
    prev_x = 0
    prev_y = 0

    # Create angles lists
    trunk_angles = []
    thigh_angles = []
    shank_angles = []
    foot_angles = []

    # Assign names to the markers in the sorted order
    for i, (y_coord, marker_id) in enumerate(sorted_yCoord):
        if i < len(names):
            name = names[i]
        else:
            name = f"Marker {i}"

        if prev_x != 0 and prev_y != 0:
            
            trunk_angle = CalcAngles(i, 0, 1, trunk_angles, centers, prev_x, prev_y)
            trunk_angle.getAngle()

            thigh_angle = CalcAngles(i, 1, 2, thigh_angles, centers, prev_x, prev_y)
            thigh_angle.getAngle()
            
            shank_angle = CalcAngles(i, 2, 3, shank_angles, centers, prev_x, prev_y)
            shank_angle.getAngle()

            if i > 3 and i <= 4:
                if (centers[i][0][1] - prev_y) != 0:
                    foot_angle = np.degrees(np.arctan((centers[i][0][0] - prev_x)/(centers[i][0][1] - prev_y)))
                    if foot_angle >= -180:
                        foot_angle = 180 - foot_angle
                    foot_angles.append(foot_angle)
   
        prev_x = centers[i][0][0]
        prev_y = centers[i][0][1]

        # Calculate hip angle
        for trunk_ang, thigh_ang, shank_ang, foot_ang in zip(trunk_angles, thigh_angles, shank_angles, foot_angles):
            hip_angle = thigh_ang - trunk_ang
            knee_angle = thigh_ang - shank_ang
            ankle_angle = foot_ang - shank_ang - 90

            if ankle_angle > 90 and ankle_angle < 180:
                ankle_angle = ankle_angle - 180
            
            # This part of the code will store the first ankle angle value.
            # The value will be stored only when the tracking starts 
            # ankle_angles list will append only the first ankle angle value
            if len(boxes) == n_markers and angle_stored == False:
                first_ankle_angle.append(ankle_angle)
                angle_stored = True

            if len(first_ankle_angle) > 0:
                ankle_angle = ankle_angle - first_ankle_angle[0]

            hip_angles.append(hip_angle)
            knee_angles.append(knee_angle)
            ankle_angles.append(ankle_angle)

            cv2.putText(frame, f"Hip Angle: {round(hip_angle, 2)}", (10, 240),cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 217), 2)
            cv2.putText(frame, f"Knee Angle: {round(knee_angle, 2)}", (10, 280),cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 217), 2)
            cv2.putText(frame, f"Ankle Angle: {round(ankle_angle, 2)}", (10, 320),cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 217), 2)

        if labels:
            for j, newbox in enumerate(boxes):
                if j == marker_id:
                    x = int(newbox[0])
                    y = int(newbox[1])
                    w = int(newbox[2])
                    h = int(newbox[3])
                    cv2.putText(frame, f"{name}", (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 128), 1)

    # Analyze the FPS rate
    fps = 1/(time() - loop_time)
    loop_time = time()

    cv2.putText(frame, f"FPS: {str(round(fps, 2))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
    cv2.putText(frame, f"Markers: {str(len(boxes))}", (10, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
    cv2.imshow('Gait analysis', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break 

camera.release()
cv2.destroyAllWindows()
