import cv2
import numpy as np

# Create a black image
img = np.zeros((720, 1200, 3), np.uint8)

# Display the image
cv2.imshow("Black Image", img)

# Wait for a key press
cv2.waitKey(0)

# Destroy all windows
cv2.destroyAllWindows()
