import cv2

# Open the webcam
cap = cv2.VideoCapture(0)  # Use 0 for default webcam, or change to a different index for a different camera

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from webcam")
        break

    # Mirror the frame horizontally
    mirrored_frame = cv2.flip(frame, 1)

    # Display the mirrored frame
    cv2.imshow('Mirrored Webcam', mirrored_frame)


    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam capture and video writer objects
cap.release()

# Close all open windows
cv2.destroyAllWindows()
