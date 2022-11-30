import cv2 as cv


class HomogeneousBgDetector():
    
    def __init__(self):
        pass

    def detect_objects(self, frame):
        # Convert Image to grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Create a Mask with adaptive threshold
        mask = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 19, 5)

        # Find contours
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        #cv2.imshow("mask", mask)
        objects_contours = []

        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > 500:
                objects_contours.append(cnt)

        return objects_contours