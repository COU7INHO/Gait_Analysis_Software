
import cv2


cap = cv2.VideoCapture("/Users/tiagocoutinho/Desktop/marcadores.MOV")


# Create the tracker object
tracker = cv2.TrackerKCF_create()

# Read the first frame of the video
success, frame = cap.read()

# Select the bounding box of the object to be tracked
bbox = cv2.selectROI(frame, False)
print(bbox)

# Initialize the tracker with the first frame and the selected bounding box
success = tracker.init(frame, bbox)

while True:
    # Read the next frame of the video
    success, frame = cap.read()

    # Update the tracker
    success, bbox = tracker.update(frame)

    # Draw the bounding box on the frame
    if success:
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Show the frame
    cv2.imshow("Tracking", frame)

    # Check if the user pressed the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()